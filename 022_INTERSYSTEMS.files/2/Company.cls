Class Shop.Company Extends (%Persistent, %Populate)
{

Property Name As %String [ Required ];

Property Phone As %String;

Property DeliveryAddress As Shop.Address;

Relationship Orders As Shop.Order [ Cardinality = many, Inverse = Customer ];

// ①

Index NameIndex On Name [ Unique ];

Method Print() As %Status
{
  write !, "Name: ", ..Name, "."
  write !, "Phone: ", ..Phone, "."
  write !, "DeliveryAddress: ", ..DeliveryAddress.City, ", ", ..DeliveryAddress.Street, ", ", ..DeliveryAddress.Zip, "."
  return $$$OK
}

Storage Default
{
<Data name="CompanyDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>Name</Value>
</Value>
<Value name="3">
<Value>Phone</Value>
</Value>
<Value name="4">
<Value>DeliveryAddress</Value>
</Value>
</Data>
<DataLocation>^Shop.CompanyD</DataLocation>
<DefaultData>CompanyDefaultData</DefaultData>
<IdLocation>^Shop.CompanyD</IdLocation>
<IndexLocation>^Shop.CompanyI</IndexLocation>
<StreamLocation>^Shop.CompanyS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
