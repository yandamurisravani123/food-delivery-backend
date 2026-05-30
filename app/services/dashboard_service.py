from app.repositories.dashboard_repository import DashboardRepository
<<<<<<< HEAD


class DashboardService:

    @staticmethod
    async def get_metrics(session, restaurant_id):

=======
 
 
class DashboardService:
 
    @staticmethod
    async def get_metrics(session, restaurant_id):
 
>>>>>>> 6da5f03 (testing)
        growth_data = await DashboardRepository.get_growth_metrics(
            session,
            restaurant_id
        )
<<<<<<< HEAD

        return growth_data

    @staticmethod
    async def repeat_orders(session, restaurant_id):

=======
 
        return growth_data
 
    @staticmethod
    async def repeat_orders(session, restaurant_id):
 
>>>>>>> 6da5f03 (testing)
        retention_data = await DashboardRepository.get_repeat_orders(
            session,
            restaurant_id
        )
<<<<<<< HEAD

        return retention_data

    @staticmethod
    async def market_reach(session, restaurant_id):

=======
 
        return retention_data
 
    @staticmethod
    async def market_reach(session, restaurant_id):
 
>>>>>>> 6da5f03 (testing)
        market_data = await DashboardRepository.get_market_reach(
            session,
            restaurant_id
        )
<<<<<<< HEAD

        return market_data

    @staticmethod
    async def rating_trend(session, restaurant_id):

=======
 
        return market_data
 
    @staticmethod
    async def rating_trend(session, restaurant_id):
 
>>>>>>> 6da5f03 (testing)
        rating_data = await DashboardRepository.get_rating_trend(
            session,
            restaurant_id
        )
<<<<<<< HEAD

        return rating_data

    @staticmethod
    async def growth_tips(session, restaurant_id):

        return {
            "tips": []
        }

    @staticmethod
    async def competitor_benchmark(session, restaurant_id):

=======
 
        return rating_data
 
    @staticmethod
    async def growth_tips(session, restaurant_id):
 
        return {
            "tips": []
        }
 
    @staticmethod
    async def competitor_benchmark(session, restaurant_id):
 
>>>>>>> 6da5f03 (testing)
        return await DashboardRepository.get_competitor_benchmark(
            session,
            restaurant_id
        )
<<<<<<< HEAD

    @staticmethod
    async def marketing_impact(session, restaurant_id):

=======
 
    @staticmethod
    async def marketing_impact(session, restaurant_id):
 
>>>>>>> 6da5f03 (testing)
        return await DashboardRepository.get_marketing_impact(
            session,
            restaurant_id
        )
<<<<<<< HEAD

    @staticmethod
    async def stock_efficiency(session, restaurant_id):

=======
 
    @staticmethod
    async def stock_efficiency(session, restaurant_id):
 
>>>>>>> 6da5f03 (testing)
        return await DashboardRepository.get_stock_efficiency(
            session,
            restaurant_id
        )
<<<<<<< HEAD

    @staticmethod
    async def staff_performance(session, restaurant_id):

=======
 
    @staticmethod
    async def staff_performance(session, restaurant_id):
 
>>>>>>> 6da5f03 (testing)
        return await DashboardRepository.get_staff_performance(
            session,
            restaurant_id
        )
<<<<<<< HEAD

    @staticmethod
    async def dashboard_summary(session, restaurant_id):

=======
 
    @staticmethod
    async def dashboard_summary(session, restaurant_id):
 
>>>>>>> 6da5f03 (testing)
        heatmap_data = await DashboardRepository.get_orders_by_time(
            session,
            restaurant_id
        )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        peak_data = await DashboardRepository.get_peak_hour_orders(
            session,
            restaurant_id
        )
<<<<<<< HEAD

        heatmap = []

        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        for row in heatmap_data:

            day_index = int(row.day)

            if 0 <= day_index <= 6:

=======
 
        heatmap = []
 
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
 
        for row in heatmap_data:
 
            day_index = int(row.day)
 
            if 0 <= day_index <= 6:
 
>>>>>>> 6da5f03 (testing)
                heatmap.append({
                    "day": days[day_index],
                    "hour": f"{int(row.hour)}:00",
                    "orders": row.orders
                })
<<<<<<< HEAD

        peak_hour = 12

        if peak_data:
            peak_hour = int(peak_data.hour)

=======
 
        peak_hour = 12
 
        if peak_data:
            peak_hour = int(peak_data.hour)
 
>>>>>>> 6da5f03 (testing)
        prep_analysis = await DashboardRepository.get_prep_analysis(
            session,
            restaurant_id
        )
<<<<<<< HEAD

        return {
            "heatmap": heatmap,

=======
 
        return {
            "heatmap": heatmap,
 
>>>>>>> 6da5f03 (testing)
            "peak_card": {
                "title": "Peak Orders",
                "peak_time": f"{peak_hour}:00 - {peak_hour + 2}:00",
                "revenue_percentage": 0
            },

            "staff_planning": {
                "suggestions": [
                    "Schedule additional staff during peak hours"
                ]
            },

            "prep_analysis": prep_analysis
<<<<<<< HEAD
        }
=======
        }
>>>>>>> 6da5f03 (testing)
