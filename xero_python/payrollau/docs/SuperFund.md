# SuperFund

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**super_fund_id** | **str** | Xero identifier for a super fund | [optional] 
**type** | [**SuperFundType**](SuperFundType.md) |  | 
**name** | **str** | Name of the super fund (max length &#x3D; 76) | [optional] 
**abn** | **str** | ABN of the self managed super fund (max length &#x3D; 11) | [optional] 
**bsb** | **str** | BSB of the self managed super fund (max length &#x3D; 6) | [optional] 
**account_number** | **str** | The account number for the self managed super fund. | [optional] 
**account_name** | **str** | The account name for the self managed super fund (max length &#x3D; 32). | [optional] 
**electronic_service_address** | **str** | The electronic service address for the self managed super fund (max length &#x3D; 16). | [optional] 
**employer_number** | **str** | Some funds assign a unique number to each employer (max length &#x3D; 20) | [optional] 
**spin** | **str** | The SPIN of the Regulated SuperFund. This field has been deprecated. It will only be present for legacy superfunds. New superfunds will not have a SPIN value. The USI field should be used instead of SPIN. | [optional] 
**usi** | **str** | The USI of the Regulated SuperFund | [optional] 
**updated_date_utc** | **datetime** | Last modified timestamp | [optional] 
**validation_errors** | [**list[ValidationError]**](ValidationError.md) | Displays array of validation error messages from the API | [optional] 

The maximum lengths above are the documented provider limits for creating a self
managed fund, except EmployerNumber, which applies to the additional fields. The
SDK does not enforce them.

[[Back to README]](../../../README.md)


