package com.ccc.spring.model;

import java.util.ArrayList;

import com.ccc.spring.dao.WriteJsonFile;

public class LiquorLicenceList {
	public ArrayList<LiquorLicence> list = new ArrayList<LiquorLicence>();

	public void addElement(String location, String sentiment, int value) {
		// System.out.println(sentiment);
		Integer index = hasElement(location);
		if (index == null) {
			list.add(new LiquorLicence(location));
			index = list.size() - 1;
		}
		
		LiquorLicence l = list.get(index);
		if (sentiment.equals("positive")) {
			l.positive += value;
		} else if (sentiment.equals("negative")) {
			l.negative += value;
		} else {
			l.neutral += value;
		}
	}

	public Integer hasElement(String location) {
		for (Integer index = 0; index < list.size(); index++) {
			if (list.get(index).location.equals(location)) {
				return index;
			}
		}
		return null;
	}

	public void getTotal() {
		for (int index = 0; index < list.size(); index++) {
			list.get(index).getTotal();
		}
	}

	public void recordData() {
		LiquorLicence ls;
		String output = "{\"data\":[";
		for (int index = 0; index < list.size() - 1; index++) {
			ls = list.get(index);
			output = output + ls.positive + ",";
		}

		output = output + list.get(list.size() - 1).positive + "]}";
		WriteJsonFile.WriteConfigJson(output, "s2/positive.json");

		output = "{\"data\":[";
		for (int index = 0; index < list.size() - 1; index++) {
			ls = list.get(index);
			output = output + ls.negative + ",";
		}

		output = output + list.get(list.size() - 1).negative + "]}";
		WriteJsonFile.WriteConfigJson(output, "s2/negative.json");

		output = "{\"data\":[";
		for (int index = 0; index < list.size() - 1; index++) {
			ls = list.get(index);
			output = output + ls.neutral + ",";
		}

		output = output + list.get(list.size() - 1).neutral + "]}";
		WriteJsonFile.WriteConfigJson(output, "s2/neutral.json");
	}

}
