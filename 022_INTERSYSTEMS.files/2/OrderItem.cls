Class Shop.OrderItem Extends (%Persistent, %Populate)
{

Relationship Product As Shop.Product [ Cardinality = many, Inverse = OrdersItems ];

Property Count As %Integer;

Relationship Order As Shop.Order [ Cardinality = parent, Inverse = Items ];

Storage Default
{
<Data name="OrderItemDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>Product</Value>
</Value>
<Value name="3">
<Value>Count</Value>
</Value>
</Data>
<DataLocation>{%%PARENT}("Items")</DataLocation>
<DefaultData>OrderItemDefaultData</DefaultData>
<IdLocation>^Shop.OrderC("Items")</IdLocation>
<IndexLocation>^Shop.OrderItemI</IndexLocation>
<StreamLocation>^Shop.OrderItemS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
