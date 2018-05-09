package com.ccc.spring.model;

public class LiquorLicence {
	public String location;
	public int positive;
	public int negative;
	public int neutral;
	public int total;
	public LiquorLicence(String loc) {
		this.location = loc;
		this.positive = 0;
		this.negative = 0;
		this.neutral = 0;
	}
	@Override
	public String toString() {
		return "LiquorLicence [location=" + location + ", positive=" + positive + ", negative=" + negative
				+ ", neutral=" + neutral + ", total=" + total + "]";
	}
	
	public void getTotal() {
		total = positive + negative + neutral;
	}
}
