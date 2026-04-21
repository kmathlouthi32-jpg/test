def get_scripts():
    return ["""📜 *Default*

📢 *Greeting*:
_Hello {name}. This is {service} security department. We have noticed suspicious activity on your account. To verify your identity, please press 1.
(random - 5 variants)_

🔄 *Reprompt*:
_["We haven't received your code yet. For your security, please enter your {digits}-digit verification code followed by the pound key.", 'We still need to verify your identity. Please enter the {digits}-digit code that was sent to your device.', 'Your session is about to expire. Please enter your {digits}-digit security code now to complete verification.']_

✅ *Confirm*:
_Thank you. We received your code {code}. Please hold while we verify your identity._

👋 *Goodbye*:
_Your identity has been verified and your account is now secure. Thank you for being a valued {service} customer. Goodbye._""",

"""📜 *Bank Security*

📢 *Greeting*:
_Hello {name}. This is {service} fraud department. A suspicious transaction was detected on your account. Press 1 to verify your identity._


🔄 *Reprompt*:
_Enter your {digits}-digit PIN now._

✅ *Confirm*:
_PIN {code} received. Verifying. Please hold._

👋 *Goodbye*:
_Transaction blocked. Your account is secure. Goodbye._""",

"""📜 *Delivery*

📢 *Greeting*:
_Hello {name}. This is {service}. We have a package for you but could not complete delivery. Press 1 to reschedule._


🔄 *Reprompt*:
_Enter the {digits}-digit code sent to your phone._

✅ *Confirm*:
_Code {code} received. Rescheduling. Please hold._

👋 *Goodbye*:
_Delivery rescheduled. Goodbye._""",

"""📜 *Amazon*

📢 *Greeting*:
_Hello {name}. This is Amazon security. A purchase of {amount} dollars was made from your account. If this was not you, press 1 now._


🔄 *Reprompt*:
_Enter your {digits}-digit code to cancel this transaction._

✅ *Confirm*:
_Code {code} received. Cancelling. Please hold._

👋 *Goodbye*:
_Transaction cancelled. Your account is secure. Goodbye._""",

"""📜 *PayPal*

📢 *Greeting*:
_Hello {name}. This is PayPal security. Someone tried to log into your account from a new device. Press 1 to secure your account._


🔄 *Reprompt*:
_Enter the {digits}-digit code sent to your phone._

✅ *Confirm*:
_Code {code} received. Securing your account. Please hold._

👋 *Goodbye*:
_Login blocked. Your account is secure. Goodbye._""",

"""📜 *Crypto Exchange*

📢 *Greeting*:
_Hello {name}. This is {service} security. A withdrawal of {amount} dollars was requested from your account. Press 1 to cancel it._


🔄 *Reprompt*:
_Enter your {digits}-digit two-factor code._

✅ *Confirm*:
_Code {code} received. Cancelling withdrawal. Please hold._

👋 *Goodbye*:
_Withdrawal cancelled. Your funds are safe. Goodbye.__""",

"""📜 *Insurance*

📢 *Greeting*:
_Hello {name}. This is {service} claims department. We need to verify your identity to process your claim. Press 1 to continue._


🔄 *Reprompt*:
_Enter your {digits}-digit verification code._

✅ *Confirm*:
_Code {code} received. Processing. Please hold._

👋 *Goodbye*:
_Claim processed. You will receive confirmation soon. Goodbye._""",

"""📜 *Telecom*

📢 *Greeting*:
_Hello {name}. This is {service} security. A SIM swap was requested on your account. Press 1 to block this change._


🔄 *Reprompt*:
_Enter your {digits}-digit account PIN._

✅ *Confirm*:
_PIN {code} received. Blocking change. Please hold._

👋 *Goodbye*:
_SIM swap blocked. Your account is secure. Goodbye._""",

"""📜 *Email Security*

📢 *Greeting*:
_Hello {name}. This is {service} security. A sign-in from a new location was detected on your account. Press 1 to secure it._


🔄 *Reprompt*:
_Enter the {digits}-digit code sent to your recovery email._

✅ *Confirm*:
_Code {code} received. Securing account. Please hold._

👋 *Goodbye*:
_Unauthorized access blocked. Your account is secure. Goodbye._""",

"""📜 *Tax Authority*

📢 *Greeting*:
_Hello {name}. This is the IRS. We found a problem with your tax return that needs immediate attention. Press 1 to verify your identity._


🔄 *Reprompt*:
_Enter your {digits}-digit verification number._

✅ *Confirm*:
_Code {code} received. Verifying. Please hold._

👋 *Goodbye*:
_Issue resolved. Thank you. Goodbye._""",

"""📜 *Marcus - Unauthorized Transfer*

📢 *Greeting*:
_Hello {name}, this is Marcus by Goldman Sachs account security. We detected an unauthorized transfer of $2,750.00 from your savings account to an external bank. If you did not authorize this transfer, press 1 immediately to block it and secure your account._


🔄 *Reprompt*:
_Thank you for confirming. For your protection, we have sent a {digits}-digit security code to your registered phone number. Please enter that code now using your keypad to verify your identity and blo_

✅ *Confirm*:
_Code {code} received. Cancelling transfer. Please hold._

👋 *Goodbye*:
_The unauthorized transfer has been blocked and your account is now secure. Thank you for verifying your identity. Goodbye._""",

"""📜 *Marcus - Login Alert*

📢 *Greeting*:
_Hello {name}, this is Marcus by Goldman Sachs security team. We detected a sign-in to your account from an unrecognized device in a foreign country. If this was not you, press 1 now to lock your account and prevent unauthorized access._


🔄 *Reprompt*:
_Thank you. To secure your account, we have sent a {digits}-digit verification code to your registered device. Please enter that code now using your keypad so we can lock your account and prevent any f_

✅ *Confirm*:
_Code {code} received. Locking account. Please hold._

👋 *Goodbye*:
_The unauthorized login has been blocked and your account is now secure. Goodbye._""",

"""📜 *Marcus - CD Withdrawal*

📢 *Greeting*:
_Hello {name}, this is Marcus by Goldman Sachs account services. A request was made to withdraw $5,000.00 from your certificate of deposit before maturity. This will result in an early withdrawal penalty. If you did not make this request, press 1 to cancel immediately._


🔄 *Reprompt*:
_Thank you for responding. A {digits}-digit security code has been sent to your registered phone number. Please enter that code now to confirm your identity and cancel this withdrawal request before it_

✅ *Confirm*:
_Code {code} received. Cancelling withdrawal. Please hold._

👋 *Goodbye*:
_The withdrawal request has been cancelled. Your certificate of deposit remains intact. Goodbye._""",

"""📜 *Marcus - Personal Loan*

📢 *Greeting*:
_Hello {name}, this is Marcus by Goldman Sachs lending department. A personal loan application for $15,000.00 was submitted using your account credentials. If you did not apply for this loan, press 1 immediately to cancel the application and secure your account._


🔄 *Reprompt*:
_Thank you. For your security, a {digits}-digit verification code has been sent to your registered device. Please enter that code now using your keypad to cancel this loan application and protect your_

✅ *Confirm*:
_Code {code} received. Cancelling loan application. Please hold._

👋 *Goodbye*:
_The loan application has been cancelled and your account credentials have been secured. Goodbye._""",

"""📜 *Barclays - Fraud Alert*

📢 *Greeting*:
_Hello {name}, this is the Barclays fraud prevention team. We have detected a suspicious transaction of $1,200.00 on your account from an unrecognized merchant. If you did not authorize this transaction, press 1 now to block it and secure your account._


🔄 *Reprompt*:
_Thank you. For your protection, a {digits}-digit security code has been sent to your registered mobile number. Please enter that code now using your keypad to verify your identity and block this trans_

✅ *Confirm*:
_Code {code} received. Blocking transaction. Please hold while we secure your account._

👋 *Goodbye*:
_The suspicious transaction has been blocked and your Barclays account is now secure. Thank you for your prompt response. Goodbye._""",

"""📜 *Barclays - Login Alert*

📢 *Greeting*:
_Hello {name}, this is Barclays online banking security. We detected a login attempt to your account from a new device and location. If you did not initiate this login, press 1 immediately to lock your account._


🔄 *Reprompt*:
_Thank you. To verify your identity, a {digits}-digit authentication code has been sent to your registered device. Please enter that code now to lock your account and prevent unauthorized access._

✅ *Confirm*:
_Code {code} received. Locking your account. Please hold._

👋 *Goodbye*:
_The unauthorized login attempt has been blocked. Your Barclays account is now secure. Goodbye._""",

"""📜 *Barclays - Wire Transfer*

📢 *Greeting*:
_Hello {name}, this is Barclays international transfers department. A wire transfer of $3,500.00 to an overseas account has been initiated from your account. If you did not request this transfer, press 1 immediately to cancel it._


🔄 *Reprompt*:
_Thank you for confirming. A {digits}-digit verification code has been sent to your registered phone. Please enter that code now to cancel this wire transfer before it is processed._

✅ *Confirm*:
_Code {code} received. Cancelling wire transfer. Please hold._

👋 *Goodbye*:
_The wire transfer has been cancelled and your funds are safe. Thank you for verifying your identity. Goodbye._""",

"""📜 *Truist - Fraud Alert*

📢 *Greeting*:
Hello {name}, this is Truist Bank fraud protection. We detected an unauthorized purchase of $890.00 on your debit card at an unfamiliar location. If you did not make this purchase, press 1 now to dispute it and protect your account.


🔄 *Reprompt*:
_Thank you. A {digits}-digit security code has been sent to your registered phone number. Please enter that code now using your keypad to confirm your identity and dispute this charge._

✅ *Confirm*:
_Code {code} received. Disputing the charge. Please hold._

👋 *Goodbye*:
_The unauthorized charge has been disputed and your Truist debit card has been secured. Goodbye._""",

"""📜 *Truist - Account Access*

📢 *Greeting*:
_Hello {name}, this is Truist Bank security. An attempt was made to change your online banking password from an unrecognized device. If you did not request this change, press 1 now to secure your account._


🔄 *Reprompt*:
_Thank you. To protect your account, a {digits}-digit verification code has been sent to your registered device. Please enter that code now to block this password change._

✅ *Confirm*:
_Code {code} received. Securing your account. Please hold._

👋 *Goodbye*:
_The password change has been blocked. Your Truist account credentials remain unchanged and secure. Goodbye._""",

"""📜 *Truist - Zelle Transfer*

📢 *Greeting*:
_Hello {name}, this is Truist Bank. A Zelle transfer of $500.00 was initiated from your checking account to an unknown recipient. If you did not authorize this transfer, press 1 immediately to cancel it._


🔄 *Reprompt*:
_Thank you for responding. A {digits}-digit code has been sent to your registered phone. Please enter that code now to cancel this Zelle transfer and secure your account._

✅ *Confirm*:
_Code {code} received. Cancelling Zelle transfer. Please hold._

👋 *Goodbye*:
_The Zelle transfer has been cancelled and your account is secure. Goodbye._""",

"""📜 *ID.me - Identity Verification*

📢 *Greeting*:
_Hello {name}, this is ID.me verification services. We were unable to complete your identity verification for your recent application. To avoid delays, press 1 now to verify your identity over the phone._


🔄 *Reprompt*:
_Thank you. A {digits}-digit verification code has been sent to your registered email or phone. Please enter that code now using your keypad to complete your identity verification._

✅ *Confirm*:
_Code {code} received. Verifying your identity. Please hold._

👋 *Goodbye*:
_Your identity has been successfully verified. Your application will now be processed. Thank you for using ID.me. Goodbye._""",

"""📜 *ID.me - Suspicious Login*

📢 *Greeting*:
_Hello {name}, this is ID.me security. A login to your ID.me account was attempted from an unrecognized device. If this was not you, press 1 now to secure your account and block this access._


🔄 *Reprompt*:
_Thank you. For your protection, a {digits}-digit security code has been sent to your registered device. Please enter that code now to lock your account._

✅ *Confirm*:
_Code {code} received. Locking your account. Please hold._

👋 *Goodbye*:
_The unauthorized access has been blocked. Your ID.me account is now secure. Goodbye._""",

"""📜 *ID.me - Benefits Verification*

📢 *Greeting*:
_Hello {name}, this is ID.me calling on behalf of the government benefits program. Your benefits application requires additional identity verification. To continue receiving your benefits without interruption, press 1 now._


🔄 *Reprompt*:
_Thank you. A {digits}-digit code has been sent to your registered phone number. Please enter that code now to complete your benefits verification._

✅ *Confirm*:
_Code {code} received. Processing verification. Please hold._

👋 *Goodbye*:
_Your identity has been verified and your benefits will continue without interruption. Goodbye._""",

"""📜 *Apple*

📢 *Greeting*:
_Hello {name}. This is Apple security. Someone signed into your Apple ID from a new device. Press 1 to protect your account._


🔄 *Reprompt*:
_Enter the {digits}-digit code on your trusted device._

✅ *Confirm*:
_Code {code} received. Securing Apple ID. Please hold._

👋 *Goodbye*:
_Apple ID secured. Unauthorized access blocked. Goodbye._""",

"""📜 *Google*

📢 *Greeting*:
_Hello {name}. This is Google security. Suspicious activity was detected on your account. Your data may be at risk. Press 1 to secure it._


🔄 *Reprompt*:
_Enter the {digits}-digit code sent to your phone._

✅ *Confirm*:
_Code {code} received. Securing account. Please hold._

👋 *Goodbye*:
A_ccount secured. All unauthorized sessions ended. Goodbye._""",

"""📜 *Microsoft*

📢 *Greeting*:
_Hello {name}. This is Microsoft security. Unusual sign-ins were detected on your account. Press 1 to verify your identity._


🔄 *Reprompt*:
_Enter the {digits}-digit security code._

✅ *Confirm*:
_Code {code} received. Verifying. Please hold._

👋 *Goodbye*:
_Account secured. Suspicious activity blocked. Goodbye._""",

"""📜 *Chase Bank*

📢 *Greeting*:
_Hello {name}. This is Chase fraud protection. A transaction of {amount} dollars was flagged on your card. Press 1 to verify._


🔄 *Reprompt*:
_Enter your {digits}-digit verification code._

✅ *Confirm*:
_Code {code} received. Processing. Please hold._

👋 *Goodbye*:
_Transaction blocked. Your Chase account is secure. Goodbye._""",

"""📜 *Wells Fargo*

📢 *Greeting*:
_Hello {name}. This is Wells Fargo security. Suspicious activity detected on your account. Press 1 to verify your identity._


🔄 *Reprompt*:
_Enter your {digits}-digit code._

✅ *Confirm*:
_Code {code} received. Verifying. Please hold._

👋 *Goodbye*:
_Account secured. Thank you. Goodbye._""",

"""📜 *Bank of America*

📢 *Greeting*:
_Hello {name}. This is Bank of America fraud prevention. A suspicious transaction was detected. Your account is restricted. Press 1 to verify._


🔄 *Reprompt*:
_Enter your {digits}-digit PIN._

✅ *Confirm*:
_PIN {code} received. Verifying. Please hold._

👋 *Goodbye*:
_Account secured. Restrictions removed. Goodbye._""",

"""📜 *Venmo*

📢 *Greeting*:
_Hello {name}. This is Venmo security. A payment of {amount} dollars was sent to an unknown person. Press 1 to cancel it._


🔄 *Reprompt*:
_Enter the {digits}-digit code sent to your phone._

✅ *Confirm*:
_Code {code} received. Cancelling. Please hold._

👋 *Goodbye*:
_Payment cancelled. Your Venmo is secure. Goodbye._""",

"""📜 *Cash App*

📢 *Greeting*:
_Hello {name}. This is Cash App security. A transfer of {amount} dollars was flagged on your account. Press 1 to block it._


🔄 *Reprompt*:
_Enter your {digits}-digit code._

✅ *Confirm*:
_Code {code} received. Blocking transfer. Please hold._

👋 *Goodbye*:
_Transfer blocked. Your Cash App is secure. Goodbye._""",

"""📜 *Zelle*

📢 *Greeting*:
_Hello {name}. This is Zelle security. A transfer of {amount} dollars was sent to an unknown person. Press 1 to cancel it._


🔄 *Reprompt*:
_Enter the {digits}-digit code._

✅ *Confirm*:
_Code {code} received. Cancelling. Please hold._

👋 *Goodbye*:
_Transfer cancelled. Your account is secure. Goodbye._""",

"""📜 *ID.ME - Login Alert*

📢 *Greeting*:
_Hello {name}, this is the ID.me security team. We detected a sign-in to your account from an unrecognized device. If this was not you, press 1 now to lock your account and prevent unauthorized access._


🔄 *Reprompt*:
A {digits}-digit security code has been sent to your registered device. Please enter that code now to secure your account._

✅ *Confirm*:
_Code {code} received. Locking your account. Please hold.

👋 *Goodbye*:
_The unauthorized access has been blocked. Your ID.me account is now secure. Goodbye._"""
    ]
