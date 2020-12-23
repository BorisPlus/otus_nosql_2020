Class Shop.Product Extends (%Persistent, %Populate)
{

Property Name As %String;

Property ProductBarCode As %String;

Property Weight As %Integer;

Property Price As %Integer;

Index ProductBarCodeIndex On ProductBarCode [ Unique ];

Relationship OrdersItems As Shop.OrderItem [ Cardinality = one, Inverse = Product ];

Storage Default
{
<Data name="ProductDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>Name</Value>
</Value>
<Value name="3">
<Value>ProductBarCode</Value>
</Value>
<Value name="4">
<Value>Weight</Value>
</Value>
<Value name="5">
<Value>Price</Value>
</Value>
<Value name="6">
<Value>OrderItem</Value>
</Value>
<Value name="7">
<Value>OrdersItems</Value>
</Value>
</Data>
<DataLocation>^Shop.ProductD</DataLocation>
<DefaultData>ProductDefaultData</DefaultData>
<IdLocation>^Shop.ProductD</IdLocation>
<IndexLocation>^Shop.ProductI</IndexLocation>
<StreamLocation>^Shop.ProductS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
