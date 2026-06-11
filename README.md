# Food Delivery Backend

Copy `.env.example` to `.env` and update the values before running the app.

The startup error you saw is caused by Postgres rejecting the credentials in `DATABASE_URL`, so make sure the password in `.env` matches your local Postgres user.

Example:

    DATABASE_URL=postgresql+asyncpg://postgres:<your_password>@localhost:5432/food_delivery
