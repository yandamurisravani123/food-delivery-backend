class CustomizationService:

    @staticmethod
    async def add_instruction(db, item_id, instruction):
        return {
            "item_id": item_id,
            "instruction": instruction,
            "status": "added"
        }
