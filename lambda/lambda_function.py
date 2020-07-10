
# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import random
import logging
import json
import prompts
import requests

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_slot_value

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class GetNewFactHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetNewFactIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        #random_fact = random.choice(data[prompts.FACTS])
        #random_fact = prompts.FACTS[1]
        random_fact = "Alice facts is listening"

        speech = data[prompts.GET_FACT_MESSAGE].format(random_fact)

        reprompt = data[prompts.HELP_REPROMPT]

        handler_input.response_builder.speak(speech).ask(
            reprompt).set_card(
            SimpleCard(data[prompts.SKILL_NAME], random_fact))
        return handler_input.response_builder.response

class GetSalesIntentHandler(AbstractRequestHandler):
    """Handler for Get Sales Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetSalesIntent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetSalesIntentHandler")
        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]
        endingSlotValue = get_slot_value(handler_input=handler_input, slot_name="endingsentence")
        if endingSlotValue:
            tempString = str(endingSlotValue)
            tempString = tempString.replace(" ","")
            tempString = tempString.lower()
            request_string = "https://us-central1-acv-data.cloudfunctions.net/hackathon?value_type=sales&relative_date_time=" + tempString
        else: 
            request_string = "https://us-central1-acv-data.cloudfunctions.net/hackathon?value_type=sales&relative_date_time=yesterday"
        '''endingSlotValue = get_slot_value(
            handler_input=handler_input, slot_name="endingsentence")
        if endingSlotValue:
            request_string = "https://us-central1-acv-data.cloudfunctions.net/hackathon?value_type=sales&relative_date_time={}".format(endingSlotValue)
        else:
            request_string = "https://us-central1-acv-data.cloudfunctions.net/hackathon?value_type=sales&relative_date_time=yesterday"'''
        #speech_text = "Yoo, we sold {} cars {}".format(data[prompts.CAR_SOLD_TODAY], endingSlotValue)
        response = requests.get(request_string)
        data1 = json.loads(response.text)
        speech_text = "We sold {0} cars {1}".format(data1["sales"], data1["period"])
        #speech_text = "We Sold {} cars Today".format(data[prompts.CAR_SOLD_TODAY])
        #speech_text = data[prompts.SALES_MESSAGE]
        reprompt = data[prompts.SALES_REPROMPT]
        handler_input.response_builder.speak(speech_text).ask(
            reprompt).set_card(SimpleCard(
                data[prompts.SKILL_NAME], speech_text))
        return handler_input.response_builder.response

class GetTitlesIntentHandler(AbstractRequestHandler):
    #Handler for GET TITLES Intent.

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetTitlesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetTitlesIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]
        
        endingSlotValue = get_slot_value(handler_input=handler_input, slot_name="ending_sentence")
        if endingSlotValue:
            tempString = str(endingSlotValue)
            tempString = tempString.replace(" ","")
            tempString = tempString.lower()
            request_string = "https://us-central1-acv-data.cloudfunctions.net/hackathon?value_type=titles&relative_date_time=" + tempString
        else: 
            request_string = "https://us-central1-acv-data.cloudfunctions.net/hackathon?value_type=titles&relative_date_time=yesterday"

        response = requests.get(request_string)
        data1 = json.loads(response.text)
        speech_text = "We processed {0} titles {1}".format(data1["titles"], data1["period"])
        
        #speech = data[prompts.TITLES_MESSAGE]
        reprompt = data[prompts.TITLES_REPROMPT]
        handler_input.response_builder.speak(speech_text).ask(
            reprompt).set_card(SimpleCard(
                data[prompts.SKILL_NAME], speech_text))
        return handler_input.response_builder.response

"""    
class GetSellThruIntent(AbstractRequestHandler):
    #Handler for GET TITLES Intent.

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetSellThruIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetSellThruIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]
        
        endingSlotValue = get_slot_value(handler_input=handler_input, slot_name="ending_sentence")
        if endingSlotValue:
            tempString = str(endingSlotValue)
            tempString = tempString.replace(" ","")
            tempString = tempString.lower()
            request_string = "https://us-central1-acv-data.cloudfunctions.net/hackathon?value_type=titles&relative_date_time=" + tempString
        else: 
            request_string = "https://us-central1-acv-data.cloudfunctions.net/hackathon?value_type=sell-thru&relative_date_time=yesterday"

        response = requests.get(request_string)
        data1 = json.loads(response.text)
        speech_text = "Sell-thru for {0} is {1}".format(data1["period"], data1["sell-thru"])
        
        reprompt = data[prompts.SELLTHRU_REPROMPT]
        handler_input.response_builder.speak(speech_text).ask(
            reprompt).set_card(SimpleCard(
                data[prompts.SKILL_NAME], speech_text))
        return handler_input.response_builder.response
"""
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        speech = data[prompts.HELP_MESSAGE]
        reprompt = data[prompts.HELP_REPROMPT]
        handler_input.response_builder.speak(speech).ask(
            reprompt).set_card(SimpleCard(
                data[prompts.SKILL_NAME], speech))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        speech = data[prompts.STOP_MESSAGE]
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        speech = data[prompts.FALLBACK_MESSAGE]
        reprompt = data[prompts.FALLBACK_REPROMPT]
        handler_input.response_builder.speak(speech).ask(
            reprompt)
        return handler_input.response_builder.response


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data.
    """

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))

        # localized strings stored in language_strings.json
        with open("language_strings.json") as language_prompts:
            language_data = json.load(language_prompts)
        # set default translation data to broader translation
        if locale[:2] in language_data:
            data = language_data[locale[:2]]
            # if a more specialized translation exists, then select it instead
            # example: "fr-CA" will pick "fr" translations first, but if "fr-CA" translation exists,
            # then pick that instead
            if locale in language_data:
                data.update(language_data[locale])
        else:
            data = language_data[locale]
        handler_input.attributes_manager.request_attributes["_"] = data


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(GetNewFactHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(GetSalesIntentHandler())
sb.add_request_handler(GetTitlesIntentHandler())
#sb.add_request_handler(GetSellThruIntent())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Register request and response interceptors
sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
