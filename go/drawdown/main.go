package main

import (
	"golang.org/x/text/language"
	"golang.org/x/text/message"
)

// Config holds all parameters for the retirement model.
type Config struct {
	Deposit      float64 // annual deposit until drawdown
	DepositRate  float64 // annual rate at which deposit grows (e.g., 0.03)
	GrowthRate   float64 // annual portfolio growth (e.g., 0.05)
	DrawdownRate float64 // annual rate at which withdrawals increase
	YearsToStart int     // years until drawdown starts
	YearsToEnd   int     // years until drawdown ends
}

// SolveInitialDrawdown returns the starting drawdown that leads to ~0 terminal balance.
// Uses binary search on the initial withdrawal value.
func SolveInitialDrawdown(cfg Config) float64 {
	// Search bounds:
	// low = 0 withdrawal
	// high = something very high (start with deposit * 10 to be safe)
	low := 0.0
	high := cfg.Deposit * 100 // very conservative upper bound

	for i := 0; i < 200; i++ { // enough iterations for high precision
		mid := (low + high) / 2
		terminal := simulate(cfg, mid)

		if terminal > 0 {
			// Too much money left — drawdown can be higher
			low = mid
		} else {
			// Ran out of money too early — drawdown must be lower
			high = mid
		}
	}

	return (low + high) / 2
}

// simulate computes the terminal balance given a starting drawdown amount.
func simulate(cfg Config, initialDraw float64) float64 {
	balance := 0.0

	// Accumulation phase
	dep := cfg.Deposit
	for year := 0; year < cfg.YearsToStart; year++ {
		balance += dep
		balance *= 1 + cfg.GrowthRate
		dep *= 1 + cfg.DepositRate
	}

	// Drawdown phase
	dd := initialDraw
	yearsDrawdown := cfg.YearsToEnd - cfg.YearsToStart

	for year := 0; year < yearsDrawdown; year++ {
		balance -= dd
		balance *= 1 + cfg.GrowthRate
		dd *= 1 + cfg.DrawdownRate
	}

	return balance
}

func main() {
	cfg := Config{
		Deposit:      508874,
		DepositRate:  20000,
		GrowthRate:   0.07,
		DrawdownRate: 0.02,
		YearsToStart: 1,
		YearsToEnd:   17,
	}

	initialDraw := SolveInitialDrawdown(cfg)

	p := message.NewPrinter(language.English)
	p.Printf("Starting annual drawdown: £%.0f\n", initialDraw)
}
