from typing import Dict


class RewardCalculator:

   
    # Calculate Order Reward Points
    # Rule: 10 points for every $1 spent
   
    @staticmethod
    def calculate_order_points(
        order_amount: float
    ) -> int:

        return int(order_amount * 10)

  
    # Calculate Remaining Points
   
    @staticmethod
    def calculate_remaining_points(
        current_points: int,
        target_points: int
    ) -> int:

        remaining = target_points - current_points

        return max(remaining, 0)

    # Calculate Progress Percentage
  
    @staticmethod
    def calculate_progress_percentage(
        current_points: int,
        target_points: int
    ) -> float:

        if target_points <= 0:
            return 0

        percentage = (
            current_points / target_points
        ) * 100

        return round(
            percentage,
            2
        )


    # Referral Reward Points
 
    @staticmethod
    def calculate_referral_points() -> int:

        return 500

    
    # Profile Completion Bonus
    # Rule: 200 points
    @staticmethod
    def calculate_profile_bonus() -> int:

        return 200


    # Reward Tier

    @staticmethod
    def get_reward_tier(
        total_points: int
    ) -> str:

        if total_points >= 5000:
            return "Elite"

        elif total_points >= 3000:
            return "Gold"

        elif total_points >= 1500:
            return "Silver"

        return "Bronze"

    
    # Reward Progress Data
   
    @staticmethod
    def get_progress_data(
        current_points: int,
        target_points: int
    ) -> Dict:

        return {
            "current_points": current_points,
            "target_points": target_points,
            "remaining_points":
                RewardCalculator.calculate_remaining_points(
                    current_points,
                    target_points
                ),
            "progress_percentage":
                RewardCalculator.calculate_progress_percentage(
                    current_points,
                    target_points
                )
        }

    # Check Redeem Eligibility
    
    @staticmethod
    def can_redeem(
        available_points: int,
        required_points: int
    ) -> bool:

        return available_points >= required_points


    # Calculate Balance After Redeem
    
    @staticmethod
    def calculate_balance_after_redeem(
        available_points: int,
        required_points: int
    ) -> int:

        if required_points > available_points:
            raise ValueError(
                "Insufficient reward points"
            )

        return available_points - required_points