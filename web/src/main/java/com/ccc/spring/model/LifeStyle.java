package com.ccc.spring.model;

public class LifeStyle {
	public String name;
	public int positive;
	public int negative;
	public int neutral;
	public int total;

	public LifeStyle(String name) {
		this.name = name;
		this.positive = 0;
		this.negative = 0;
		this.neutral = 0;
	}

	public void getTotal() {
		total = positive + negative + neutral;
	}
	
	@Override
	public String toString() {
		return "LifeStyle [name=" + name + ", positive=" + positive + ", negative=" + negative + ", neutral=" + neutral
				+ "]";
	}

}
