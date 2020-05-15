#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MichaelBotAppId")
    if not APP_ID:
        raise ValueError("Need to define LUIS_APP_ID environment variable")

    APP_PASSWORD = os.environ.get("MichaelBotAppPassword")
    if not APP_PASSWORD:
        raise ValueError("Need to define LUIS_APP_ID environment variable")

    LUIS_APP_ID = os.environ.get("LUIS_APP_ID")
    if not LUIS_APP_ID:
        raise ValueError("Need to define LUIS_APP_ID environment variable")

    LUIS_RUNTIME_KEY = os.environ.get("LUIS_RUNTIME_KEY")
    if not LUIS_RUNTIME_KEY:
        raise ValueError("Need to define LUIS_RUNTIME_KEY environment variable")

    LUIS_ENDPOINT = "https://westus.api.cognitive.microsoft.com/luis/v2.0"
