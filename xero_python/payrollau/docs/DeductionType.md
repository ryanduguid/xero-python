# DeductionType

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the deduction type (max length &#x3D; 50) | [optional]
**account_code** | **str** | See Accounts | [optional] 
**reduces_tax** | **bool** | Indicates that this is a pre-tax deduction that will reduce the amount of tax you withhold from an employee. | [optional] 
**reduces_super** | **bool** | Most deductions don’t reduce your superannuation guarantee contribution liability, so typically you will not set any value for this. | [optional] 
**is_exempt_from_w1** | **bool** | Boolean to determine if the deduction type is reportable or exempt from W1 | [optional] 
**deduction_type_id** | **str** | Xero identifier | [optional] 
**updated_date_utc** | **datetime** | Last modified timestamp | [optional] 
**deduction_category** | **str** |  | [optional] 
**current_record** | **bool** | Is the current record | [optional] 

[[Back to README]](../../../README.md)


