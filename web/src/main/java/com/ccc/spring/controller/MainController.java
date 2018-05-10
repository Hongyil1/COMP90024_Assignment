/**
 *  Xiaolu Zhang 886161
 *  Jianbo Ma 807590
 *  Hongyi Lin 838776
 *  Xiaoyu Wang 799778
 *  Shalitha Weerakoon Karunatilleke 82237
 *  COMP90024 Cluster and Cloud Computing
 *  Social Media Analytics on Melbourne & Sydney
 */

package com.ccc.spring.controller;

import java.util.ArrayList;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.ccc.spring.dao.CouchConnector;
import com.ccc.spring.model.CrimeList;
import com.ccc.spring.model.LifeStyleList;
import com.ccc.spring.model.LiquorLicenceList;
import com.ccc.spring.model.PopularTwitter;
import com.google.gson.JsonObject;

@Controller
public class MainController {
	CouchConnector c = new CouchConnector();

	@RequestMapping(value = "/scenario1", method = RequestMethod.GET)
	public String showScenarioOne(Model model) {
		scenario1("scenario/scenario1_melbourne", "melb");
		scenario1("scenario/scenario1_melbourne", "sydney");
		return "scenario1";
	}

	@RequestMapping(value = "/scenario2", method = RequestMethod.GET)
	public String showScenarioTwo(Model model) {
		scenario2();
		return "scenario2";
	}

	@RequestMapping(value = "/scenario3", method = RequestMethod.GET)
	public String showScenarioThree(Model model) {
		scenario3();
		return "scenario3";
	}

	@RequestMapping(value = "/scenario4", method = RequestMethod.GET)
	public String showScenarioFour(Model model) {
		return "scenario4";
	}

	@RequestMapping(value = "/scenario5", method = RequestMethod.GET)
	public String showScenarioFive(Model model) {
		scenario5("scenario/scenario5");
		return "scenario5";
	}

	@RequestMapping(value = "/melbmap", method = RequestMethod.GET)
	public String showMelbMap(Model model) {
		return "melbmap";
	}

	@RequestMapping(value = "/sydneymap", method = RequestMethod.GET)
	public String showSydneyMap(Model model) {
		return "sydneymap";
	}

	@RequestMapping(value = "/fetching", method = RequestMethod.GET)
	public String fetchData(Model model) {
		scenario1("scenario/scenario1_melbourne", "melb");
		scenario1("scenario/scenario1_melbourne", "syd");
		return "scenario1";
	}

	private void scenario1(String view, String path) {
		LifeStyleList list = new LifeStyleList();
		ArrayList<JsonObject> res = (ArrayList<JsonObject>) c.getView("processed_data", view);
		System.out.println("***" + view);
		for (int i = 0; i < res.size() / 3; i++) {
			list.lifeStyleList.get(i).negative = res.get(i).get("value").getAsInt();
		}
		for (int i = res.size() / 3; i < res.size() / 3 * 2; i++) {
			list.lifeStyleList.get(i - 9).neutral = res.get(i).get("value").getAsInt();
		}
		for (int i = res.size() / 3 * 2; i < res.size(); i++) {
			list.lifeStyleList.get(i - 18).positive = res.get(i).get("value").getAsInt();
		}
		list.recordData(path);
	}

	private void scenario5(String view) {
		PopularTwitter pt = new PopularTwitter();
		ArrayList<JsonObject> res = (ArrayList<JsonObject>) c.getView("processed_data", view);
		pt.positive = res.get(2).get("value").getAsInt();
		pt.negative = res.get(0).get("value").getAsInt();
		pt.neutral = res.get(1).get("value").getAsInt();
		pt.recordData();
	}

	private void scenario3() {
		CrimeList cl = new CrimeList();
		ArrayList<JsonObject> res = (ArrayList<JsonObject>) c.getView("processed_data", "scenario/scenario3");
		for (int index = 0; index < res.size(); index++) {
			String loc = res.get(index).get("key").getAsString();
			int value = res.get(index).get("value").getAsInt();
			cl.addElement(loc, value);
		}
		cl.recordData("tweeter");
	}

	private void scenario2() {
		LiquorLicenceList list = new LiquorLicenceList();
		ArrayList<JsonObject> res = (ArrayList<JsonObject>) c.getView("processed_data", "scenario/scenario2");
		for (int index = 0; index < res.size(); index++) {
			String loc = res.get(index).get("key").getAsJsonArray().get(1).getAsString();
			String sentiment = res.get(index).get("key").getAsJsonArray().get(0).getAsString();
			int value = res.get(index).get("value").getAsInt();
			System.out.println(loc + sentiment + value);
			list.addElement(loc, sentiment, value);
		}
		list.getTotal();
		System.out.println(list.list);
		list.recordData();
	}
}
