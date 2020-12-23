Class Shop.Order Extends (%Persistent, %Populate)
{

Property OrderDate As %TimeStamp;

Property State As %String;

Relationship Customer As Shop.Company [ Cardinality = one, Inverse = Orders ];

Relationship Items As Shop.OrderItem [ Cardinality = children, Inverse = Order ];

Storage Default
{
<Data name="OrderDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>OrderDate</Value>
</Value>
<Value name="3">
<Value>State</Value>
</Value>
<Value name="4">
<Value>Customer</Value>
</Value>
</Data>
<DataLocation>^Shop.OrderD</DataLocation>
<DefaultData>OrderDefaultData</DefaultData>
<IdLocation>^Shop.OrderD</IdLocation>
<IndexLocation>^Shop.OrderI</IndexLocation>
<StreamLocation>^Shop.OrderS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
