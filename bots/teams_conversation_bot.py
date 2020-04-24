# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import CardFactory, TurnContext, MessageFactory
from botbuilder.core.teams import TeamsActivityHandler, TeamsInfo
from botbuilder.schema import CardAction, HeroCard, Mention, ConversationParameters, Activity, ActivityTypes
from botbuilder.schema._connector_client_enums import ActionTypes



class TeamsConversationBot(TeamsActivityHandler):
    def __init__(self, app_id: str, app_password: str):
        self._app_id = app_id
        self._app_password = app_password

    async def on_message_activity(self, turn_context: TurnContext):
        TurnContext.remove_recipient_mention(turn_context.activity)
        turn_context.activity.text = turn_context.activity.text.strip()

        await turn_context.send_activities([
                Activity(
                    type=ActivityTypes.typing
                )
        ])

        if turn_context.activity.text.lower() == "olá" or turn_context.activity.text.lower() == "boa tarde" or turn_context.activity.text.lower() == "bom dia":
            await self._mention_activity(turn_context)
            return

        if turn_context.activity.text.lower() == "michael!":
            await self._show_members(turn_context)
            return

        if turn_context.activity.text == "UpdateCardAction":
            await self._update_card_activity(turn_context)
            return

        if turn_context.activity.text == "MessageAllMembers":
            await self._message_all_members(turn_context)
            return

        if turn_context.activity.text == "Delete":
            await self._delete_card_activity(turn_context)
            return

        card = HeroCard(
            title="O que você quer?",
            text="Tenho algumas sugestões...",
            buttons=[
                CardAction(
                    type=ActionTypes.message_back,
                    title="Update Card",
                    text="UpdateCardAction",
                    value={"count": 0},
                )
            ],
        )
        await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(card))
        )
        return

    async def _mention_activity(self, turn_context: TurnContext):
        mention = Mention(
            mentioned=turn_context.activity.from_property,
            text=f"<at>{turn_context.activity.from_property.name}</at>",
            type="mention",
        )

        reply_activity = MessageFactory.text(f"{turn_context.activity.text} {mention.text}")
        reply_activity.entities = [Mention().deserialize(mention.serialize())]
        await turn_context.send_activity(reply_activity)

    async def _update_card_activity(self, turn_context: TurnContext):
        data = turn_context.activity.value
        data["count"] += 1

        card = CardFactory.hero_card(
            HeroCard(
                title="Bem-vindo",
                text=f"Você foi cumprimentado {data['count']} vezes...",
                buttons=[
                    CardAction(
                        type=ActionTypes.message_back,
                        title="Update Card",
                        value=data,
                        text="UpdateCardAction",
                    ),
                    CardAction(
                        type=ActionTypes.message_back,
                        title="Envia para todos",
                        value=data,
                        text="MessageAllMembers",
                    ),
                    CardAction(
                        type=ActionTypes.message_back,
                        title="Retira o que disse",
                        text="Delete",
                    ),
                ],
            )
        )

        updated_activity = MessageFactory.attachment(card)
        updated_activity.id = turn_context.activity.reply_to_id
        await turn_context.update_activity(updated_activity)

    async def _message_all_members(self, turn_context: TurnContext):
        team_members = await TeamsInfo.get_members(turn_context)

        for member in team_members:
            conversation_reference = TurnContext.get_conversation_reference(
                turn_context.activity
            )

            conversation_parameters = ConversationParameters(
                is_group=False,
                bot=turn_context.activity.recipient,
                members=[member],
                tenant_id=turn_context.activity.conversation.tenant_id,
            )

            async def get_ref(tc1):
                conversation_reference_inner = TurnContext.get_conversation_reference(
                    tc1.activity
                )
                return await tc1.adapter.continue_conversation(
                    conversation_reference_inner, send_message, self._app_id
                )

            async def send_message(tc2: TurnContext):
                return await tc2.send_activity(
                    f"Hello {member.name}. I'm a Teams conversation bot."
                )  # pylint: disable=cell-var-from-loop

            await turn_context.adapter.create_conversation(
                conversation_reference, get_ref, conversation_parameters
            )

        await turn_context.send_activity(
            MessageFactory.text("All messages have been sent")
        )

    async def _delete_card_activity(self, turn_context: TurnContext):
        await turn_context.delete_activity(turn_context.activity.reply_to_id)

    async def _show_details(self, turn_context: TurnContext):
        team_details = await TeamsInfo.get_team_details(turn_context)
        print("XUNDA!")
        print(turn_context)
        reply = MessageFactory.text(f"The team name is {team_details.name}. The team ID is {team_details.id}. The AADGroupID is {team_details.aad_group_id}.")
        await turn_context.send_activity(reply)

    async def _show_members(self, turn_context: TurnContext):
        members = await TeamsInfo.get_team_members(turn_context)
        print(members)
        reply = MessageFactory.text(f"The team name is {members}. The team ID is {members.id}. The AADGroupID is {members.aad_group_id}.")
        await turn_context.send_activity(reply)