# Plan

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier of the plan | 
**name** | **str** | The name of the plan. It is used in the invoice line item description.  | 
**status** | **str** | Status of the plan. Available statuses are ACTIVE, CANCELED, and PENDING_ACTIVATION.  | 
**subscription_items** | [**list[SubscriptionItem]**](SubscriptionItem.md) | List of the subscription items belonging to the plan. It does not include cancelled subscription items.  | 

[[Back to README]](../../../README.md)


