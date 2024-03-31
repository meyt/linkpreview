def firefox():
    # v115.8
    return {
        "accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "accept-language": "en-US,en;q=0.5",
        "dnt": "1",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": (
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) "
            "Gecko/20100101 Firefox/115.0"
        ),
    }


def chrome():
    # v122
    return {
        "accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,image/apng,*/*;"
            "q=0.8,application/signed-exchange;v=b3;q=0.7"
        ),
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": (
            '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"'
        ),
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
    }


def googlebot():
    return {
        "accept": "text/plain,text/html,*/*",
        "user-agent": (
            "Mozilla/5.0 (compatible; Googlebot/2.1; "
            "+http://www.google.com/bot.html)"
        ),
    }


def twitterbot():
    return {
        "accept": "text/plain,text/html,*/*",
        "user-agent": "Twitterbot/1.0",
    }


def telegrambot():
    return {
        "accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        ),
        "accept-language": "en-US,en;q=0.5",
        "cookie": (
            "euConsent=true; BCPermissionLevel=PERSONAL; BC_GDPR=11111; "
            "fhCookieConsent=true; gdpr-source=GB; gdpr_consent=YES; "
            "beget=begetok"
        ),
        "user-agent": "TelegramBot (like TwitterBot)",
    }


def imessagebot():
    return {
        "accept": "text/plain,text/html,*/*",
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) "
            "AppleWebKit/601.2.4 (KHTML, like Gecko) Version/9.0.1 "
            "Safari/601.2.4 facebookexternalhit/1.1 Facebot Twitterbot/1.0"
        ),
    }


headers_map = dict(
    firefox=firefox,
    chrome=chrome,
    googlebot=googlebot,
    twitterbot=twitterbot,
    telegrambot=telegrambot,
    imessagebot=imessagebot,
)
