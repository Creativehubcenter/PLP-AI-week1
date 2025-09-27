# crypto_buddy.py
# Beginner-friendly rule-based crypto advisor chatbot
# Paste into a Jupyter cell or a .py file and run.

crypto_db = {
    "Bitcoin": {
        "price_trend": "rising",
        "market_cap": "high",
        "energy_use": "high",
        "sustainability_score": 3/10  # 0.3
    },
    "Ethereum": {
        "price_trend": "stable",
        "market_cap": "high",
        "energy_use": "medium",
        "sustainability_score": 6/10  # 0.6
    },
    "Cardano": {
        "price_trend": "rising",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 8/10  # 0.8
    }
}

class CryptoBuddy:
    def __init__(self, db=None, name="CryptoBuddy", tone="friendly"):
        self.db = db or {}
        self.name = name
        self.tone = tone
        self.disclaimer = ("Not financial advice. Crypto is risky—always do your own research (DYOR).")

    def greet(self):
        return f"Hey — I'm {self.name}! 🌟 Ask me about trending coins, sustainability, or which crypto might fit long-term goals."

    # Utilities
    def _find_coin(self, query_lower):
        for coin in self.db.keys():
            if coin.lower() in query_lower:
                return coin
        return None

    def _most_sustainable(self):
        best = max(self.db.items(), key=lambda kv: kv[1].get("sustainability_score", 0))
        name, data = best
        score = data["sustainability_score"]
        return f"Most sustainable: {name} — sustainability score {score:.2f}/1.0 ({score*10:.0f}/10)."

    def _trending_up(self):
        rising = [name for name, d in self.db.items() if d.get("price_trend","").lower()=="rising"]
        if not rising:
            return "No coins in the sample DB are currently 'rising'."
        return "Trending up: " + ", ".join(rising)

    def _coin_details(self, coin):
        if coin not in self.db:
            return f"No data for '{coin}'. Try: {', '.join(sorted(self.db.keys()))}"
        d = self.db[coin]
        return (f"{coin} — trend: {d['price_trend']}, market cap: {d['market_cap']}, "
                f"energy use: {d['energy_use']}, sustainability: {d['sustainability_score']*10:.0f}/10")

    def _recommend_long_term(self):
        candidates = []
        for name, d in self.db.items():
            trend = d.get("price_trend","").lower()
            mcap = d.get("market_cap","").lower()
            sustain = float(d.get("sustainability_score", 0))
            energy = d.get("energy_use","").lower()

            mcap_score = {"high":1.0, "medium":0.6, "low":0.3}.get(mcap, 0.5)
            trend_score = {"rising":1.0, "stable":0.5, "falling":0.0}.get(trend, 0.5)
            energy_score = {"low":1.0, "medium":0.6, "high":0.2}.get(energy, 0.6)

            combined = 0.5 * sustain + 0.35 * mcap_score + 0.15 * trend_score
            candidates.append((combined, name, d, mcap_score, trend_score, energy_score))

        candidates.sort(reverse=True, key=lambda x:x[0])

        for combined, name, d, mc, ts, es in candidates:
            if d.get("price_trend","").lower()=="rising" and d.get("market_cap","").lower()=="high":
                reason = (f"{name} has rising trend and high market cap — sustainability {d['sustainability_score']*10:.0f}/10.")
                return f"Recommended for long-term growth: {name}. {reason} {self.disclaimer}"

        for combined, name, d, mc, ts, es in candidates:
            if d.get("energy_use","").lower()=="low" and d.get("sustainability_score",0) > 0.7:
                reason = (f"{name} is energy-efficient and scores {d['sustainability_score']*10:.0f}/10 on sustainability.")
                return f"Recommended for long-term, sustainability-focused investors: {name}. {reason} {self.disclaimer}"

        top = candidates[0]
        name = top[1]
        return (f"Top suggestion (balanced): {name}. Combined heuristic score: {top[0]:.2f}. "
                f"Details: {self._coin_details(name)} {self.disclaimer}")

    def help_text(self):
        return ("Try queries like:\n"
                "- 'Which crypto is trending up?'\n"
                "- 'What’s the most sustainable coin?'\n"
                "- 'Which coin should I buy for long-term growth?'\n"
                "- 'Tell me about Cardano'\n"
                "- 'List coins'")

    def respond(self, user_query):
        q = (user_query or "").strip()
        ql = q.lower()
        if not q:
            return "Say something about crypto — try 'help' for examples."

        coin = self._find_coin(ql)

        if any(word in ql for word in ["help", "examples"]):
            return self.help_text()

        if any(word in ql for word in ["sustain", "eco", "green"]):
            return self._most_sustainable() + " " + self.disclaimer

        if any(word in ql for word in ["trend", "trending", "trending up", "trending down", "which is trending"]):
            return self._trending_up() + " " + self.disclaimer

        if any(word in ql for word in ["long-term", "long term", "buy for long", "buy for long-term", "which should i buy for long-term", "which crypto should i buy for long-term"]):
            return self._recommend_long_term()

        if any(word in ql for word in ["recommend", "should i buy", "which should i buy", "what should i buy", "best coin"]):
            if coin:
                return ("If you're asking about " + coin + ": " + self._coin_details(coin) + " " + self.disclaimer)
            return self._recommend_long_term()

        if any(word in ql for word in ["list", "coins", "available"]):
            return "Coins in DB: " + ", ".join(sorted(self.db.keys()))

        if any(word in ql for word in ["tell me about", "info", "details", "what is", "who is"]) and coin:
            return self._coin_details(coin) + " " + self.disclaimer

        if coin and any(word in ql for word in ["sustain", "energy", "eco", "green"]):
            d = self.db[coin]
            return f"{coin} sustainability: {d.get('sustainability_score',0)*10:.0f}/10; energy use: {d.get('energy_use')}."

        if coin:
            return self._coin_details(coin) + " " + self.disclaimer

        if any(word in ql for word in ["most", "best", "top"]):
            return self._recommend_long_term()

        return ("Sorry, I didn't quite catch that. Try 'help' for example questions. " + self.disclaimer)


if __name__ == "__main__":
    bot = CryptoBuddy(db=crypto_db)
    print(bot.greet())
    print("Type 'quit' to exit, 'help' for examples.\n")
    while True:
        try:
            q = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        if q.lower() in ("quit","exit","bye"):
            print(f"{bot.name}: Bye — and remember: {bot.disclaimer}")
            break
        print(f"{bot.name}: {bot.respond(q)}\n")
