class Price:
    current_price = 1.5
    location_factor = 1.0
    rate_history_factor = 1.0
    gallon_request_factor = 1.0
    company_profit_factor = 1.0

    def suggest_price(self):
        return self.current_price + self.margin()

    def margin(self):
        return self.current_price * (
            self.location_factor
            - self.rate_history_factor
            + self.gallon_request_factor
            + self.company_profit_factor
        )
