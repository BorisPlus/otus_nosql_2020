Class Shop.Address Extends (%SerialObject, %Populate)
{

Property Street As %String;

Property City As %String;

Property Zip As %String;

Storage Default
{
<Data name="AddressState">
<Value name="1">
<Value>Street</Value>
</Value>
<Value name="2">
<Value>City</Value>
</Value>
<Value name="3">
<Value>Zip</Value>
</Value>
</Data>
<State>AddressState</State>
<StreamLocation>^Shop.AddressS</StreamLocation>
<Type>%Storage.Serial</Type>
}

}
