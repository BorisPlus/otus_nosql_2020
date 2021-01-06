# Tarantool

Необходимо написать на тарантуле биллинг реального времени облачной системы. 
Должны быть хранимые процедуры:
- добавление денег на баланс;
- изменение расхода денег в секунду.

Когда баланс становится равным нулю, тарантул по http должен сделать GET-запрос на какой-либо внешний урл, где передать userID пользователя, у которого кончились деньги (запрос на отключение виртуальных машин). Этот вызов должен происходить как можно быстрее после окончания денег на счете.

Для реализации рекомендуется использовать библиотеку expirationd.

Использовать шардинг на основе vshard.

__Не понятна формулировка ДЗ__: 
1. "изменение расхода денег __в секунду__" - нужно сделать `что-то рандомно пополняющее\снижающее баланс рандомного пользователя`?
2. `expirationd` и `vshard` - мне не понятно назначение. То есть на основе `expirationd` нужно сделать `что-то рандомно пополняющее\снижающее баланс`?


## Реализация

```bash
docker run \
  --name mytarantool \
  -d -p 3301:3301 \
  -v /media/otus_022/opt_tarantool/app.lua:/opt/tarantool/app.lua \
  -v /media/otus_022/var_lib_tarantool:/var/lib/tarantool \
  tarantool/tarantool:2.6.0
```

```bash
docker exec -i -t mytarantool console

connected to unix/:/var/run/tarantool/tarantool.sock
unix/:/var/run/tarantool/tarantool.sock> 
```

Создаем или выбираем существующий `space`
```bash
billing = box.schema.space.create('billing', {if_not_exists=true});
balance = box.schema.space.create('balance', {if_not_exists=true});
```

Определяем поля
```bash
balance:format({
    {name = 'username', type = 'string'},
    {name = 'coins', type = 'unsigned'}
});
balance:create_index(
   'primary', {
       type = 'hash',
       parts = {'username'}
   }
);

billing:format({
    {name = 'id', type = 'integer'},
    {name = 'datetime', type = 'unsigned'},
    {name = 'username', type = 'string'},
    {name = 'balance_before', type = 'unsigned'},
    {name = 'operation', type = 'integer'},
    {name = 'balance_after', type = 'unsigned'},
    {name = 'message', type = 'string'}
});
---
...

billing:create_index(
   'primary', {
       type = 'tree',
       parts = {'id'}
   }
);
---
- unique: true
  parts:
  - type: unsigned
    is_nullable: false
    fieldno: 1
  id: 0
  space_id: 515
  type: TREE
  name: primary
  
box.space.billing:auto_increment{'id'}
billing:auto_increment{'id'};
               
    - unique: true
      parts:
      - type: string
        is_nullable: false
        fieldno: 1
      id: 0
      space_id: 512
      type: HASH
      name: primary
```

### Просто для наполнения

```bash
s:insert{'user_01', 100}
s:insert{'user_02', 200}
s:insert{'user_03', 50}
s:select{'user_03'}

    ---
    - - ['user_03', 50]

s:upsert({'user_04', 400},{{"+", 2, 2}})
s:update({'user_03'}, {{'+', 2, 700}})

s:select{}

    ---
    - - ['user_01', 100]
      - ['user_02', 200]
      - ['user_04', 400]
      - ['user_03', 750]
    ...
```

### Функция добавление денег на баланс

```bash
function increase_balance(user, coins)
    box.space.billing:update({user}, {{'+', 2, coins}})
end

increase_balance('user_03', 500)

s:select{}

---
- - ['user_01', 100]
  - ['user_02', 200]
  - ['user_04', 400]
  - ['user_03', 1250]
...

```

### Функция списания денег

```bash
function decrease_balance(user, coins)
    local current_balance = box.space.billing:select{user}[1][2] 
    if( current_balance < coins ) then 
        -- послать что не достаточно средств
        return string.format("не достаточно средств: %s, необходимо еще: %s, операция не будет совершена.", current_balance, coins - current_balance)
    end
    box.space.billing:update({user}, {{'-', 2, coins}})
    if( current_balance == coins ) then 
        -- послать что средства только что закончились
        return string.format("средства только что закончились")
    end
    -- остаток на счете
    return string.format("остаток средств: %s", current_balance - coins)
end

s:update({'user_03'}, {{'=', 2, 750}})
---
- ['user_03', 750]
...

decrease_balance('user_03', 200)
---
- 'остаток средств: 550'
...

decrease_balance('user_03', 500)
---
- 'остаток средств: 50'
...

decrease_balance('user_03', 200)
---
- 'не достаточно средств: 50, необходимо еще: 150, операция не будет совершена.'

decrease_balance('user_03', 50)
---
- средства только что закончились

...
```

### Уведомление внешнего HTTP-сервиса

Функция `notify`, которая посылает `POST` на условный 
внешний HTTP-сервис уведомление о состоянии баланса пользователя при операции списания. 

__Замечание__: не нашел, как передать POST параметры :( . В привычном виде, это что-то типа ключ-значение `{message=message, user=user}`, вообще возможно ?

```bash
function notify(user, message)
    http_client = require('http.client').new()
    local body = string.format("user=%s&message=%s", user, message)
    http_client:post("http://api.billing.coin/notify", body)
end

function decrease_balance(user, coins)
    local current_balance = box.space.billing:select{user}[1][2] 
    if( current_balance < coins ) then 
        -- послать что не достаточно средств
        local message = string.format("не достаточно средств: %s, необходимо еще: %s, операция не будет совершена.", current_balance, coins - current_balance)
        notify(user, message)
        return message
    end
    box.space.billing:update({user}, {{'-', 2, coins}})
    if( current_balance == coins ) then 
        -- послать что средства только что закончились
        local message = string.format("средства только что закончились")
        notify(user, message)
        return message
    end    -- остаток на счете

    local message = string.format("остаток средств: %s", current_balance - coins)
    notify(user, message)
    return message
end

```