# LeaveApplication

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**leave_application_id** | **str** | The Xero identifier for the leave application | [optional]
**employee_id** | **str** | The Xero identifier for Payroll Employee | [optional] 
**leave_type_id** | **str** | The Xero identifier for Leave Type | [optional] 
**title** | **str** | The title of the leave | [optional] 
**start_date** | **date** | Start date of the leave (YYYY-MM-DD) | [optional] 
**end_date** | **date** | End date of the leave (YYYY-MM-DD) | [optional] 
**description** | **str** | The Description of the Leave | [optional] 
**pay_out_type** | [**PayOutType**](PayOutType.md) |  | [optional] 
**leave_periods** | [**list[LeavePeriod]**](LeavePeriod.md) |  | [optional] 
**updated_date_utc** | **datetime** | Last modified timestamp | [optional] 
**validation_errors** | [**list[ValidationError]**](ValidationError.md) | Displays array of validation error messages from the API | [optional] 

[[Back to README]](../../../README.md)


