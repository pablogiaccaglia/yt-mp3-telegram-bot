# -*- coding: utf-8 -*-
"""
@author: pablo

"""

from telegram.ext import ConversationHandler

# different constants to easily store user data in context.user_data (persistent dict across conversations)
(
    CHAT_ID,
    MSG_ID,  # bot's message id, useful for deleting it via delete_message
    START_OVER,
) = map(chr, range(3))

# State definitions for top level conversation
HANDLE_NAME = map(chr, range(3, ))

# Shortcut for ConversationHandler.END
END = ConversationHandler.END
