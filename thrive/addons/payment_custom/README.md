# Custom Payment Modes

## Technical details

This module does not integrate with an API and, instead, offers a base for implementing payment
providers with custom payment flows relying on payment instructions being displayed to the customer.
This is done by immediately marking transactions as 'pending' to display their 'pending message'.

It defines a base Wire Transfer payment provider that allows making payments by bank transfer.

## Supported features

- Direct payment flow

## Module history

- `16.1`
  - The default payment instructions message of Wire Transfer can be recomputed at any time after
    installation of the module. thrive/thrive#103903
- `16.0`
  - The `custom_mode` field is added to distinguish custom payment modes from other payment
    providers and to allow duplicating the base Wire Transfer provider in multi-company databases.
    thrive/thrive#99400
  - The module is no longer automatically installed with the `payment` module. thrive/thrive#99400
  - The module is renamed from `payment_transfer` to `payment_custom`. thrive/thrive#99400

## Testing instructions

Wire Transfer can be tested indifferently in test or live mode as it does not make API requests.
