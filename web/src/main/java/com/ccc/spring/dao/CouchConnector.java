package com.ccc.spring.dao;

import java.util.ArrayList;
import java.util.List;

import org.lightcouch.CouchDbClient;
import org.lightcouch.CouchDbProperties;

import com.ccc.spring.model.CrimeList;
import com.ccc.spring.model.LifeStyleList;
import com.ccc.spring.model.PopularTwitter;
import com.google.gson.JsonObject;

public class CouchConnector {
	public static final String dbAddr = "127.0.0.1";
	public static final String dbUser = "admin";
	public static final String dbPassword = "admin";

	public List<JsonObject> getView(String dbName, String viewName) {
		CouchDbProperties properties = new CouchDbProperties().setDbName(dbName).setCreateDbIfNotExist(true)
				.setProtocol("http").setHost(dbAddr).setPort(5984).setMaxConnections(100).setUsername(dbUser)
				.setPassword(dbPassword).setConnectionTimeout(0);
		CouchDbClient dbClient = new CouchDbClient(properties);
		List<JsonObject> allDocs = dbClient.view(viewName).group(true).query(JsonObject.class);
		dbClient.shutdown();
		return allDocs;
	}

	public List<JsonObject> getAllDocs(String dbName) {
		CouchDbProperties properties = new CouchDbProperties().setDbName(dbName).setCreateDbIfNotExist(true)
				.setProtocol("http").setHost(dbAddr).setPort(5984).setMaxConnections(100).setUsername(dbUser)
				.setPassword(dbPassword).setConnectionTimeout(0);

		CouchDbClient dbClient = new CouchDbClient(properties);

		List<JsonObject> allDocs = dbClient.view("_all_docs").includeDocs(true).query(JsonObject.class);
		dbClient.shutdown();
		return allDocs;
	}

	// public static void main(String[] args) {
	// CouchConnector c = new CouchConnector();
	// String jsonOutput = c.getView("processed_data",
	// "scenario/scenario3").toString();
	// System.out.println(c.getView("processed_data", "scenario/scenario3").size());
	// System.out.println("***" + jsonOutput);
	//
	// // PopularTwitter pt = new PopularTwitter();
	// // ArrayList<JsonObject> res = (ArrayList<JsonObject>)
	// // couchdb.getView("processed_data", view);
	// // pt.positive = res.get(2).get("value").getAsInt();
	// // pt.negative = res.get(0).get("value").getAsInt();
	// // pt.neutral = res.get(1).get("value").getAsInt();
	// // pt.recordData();
	// // System.out.println("123");
	//
	//// LiquorLicenceList list = new LiquorLicenceList();
	//// ArrayList<JsonObject> res = (ArrayList<JsonObject>)
	// c.getView("processed_data", "scenario/scenario2");
	//// for (int index = 0; index < res.size(); index++) {
	//// String loc =
	// res.get(index).get("key").getAsJsonArray().get(1).getAsString();
	//// String sentiment =
	// res.get(index).get("key").getAsJsonArray().get(0).getAsString();
	//// int value = res.get(index).get("value").getAsInt();
	//// System.out.println(loc + sentiment + value);
	//// list.addElement(loc, sentiment, value);
	//// }
	//// list.getTotal();
	//// System.out.println(list.list);
	//// list.recordData();
	//// c.scenario1(c, "scenario/scenario1_melbourne", "melb");
	//// c.scenario1(c, "scenario/scenario1_melbourne", "syd");
	//// c.scenario5(c, "scenario/scenario5");
	// }

	public void scenario1(CouchConnector couchdb, String view, String path) {
		LifeStyleList list = new LifeStyleList();
		ArrayList<JsonObject> res = (ArrayList<JsonObject>) couchdb.getView("processed_data", view);

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

	public void scenario5(CouchConnector couchdb, String view) {
		PopularTwitter pt = new PopularTwitter();
		ArrayList<JsonObject> res = (ArrayList<JsonObject>) couchdb.getView("processed_data", view);
		pt.positive = res.get(2).get("value").getAsInt();
		pt.negative = res.get(0).get("value").getAsInt();
		pt.neutral = res.get(1).get("value").getAsInt();
		pt.recordData();
	}

	public static void main(String[] args) {
		CouchConnector c = new CouchConnector();
		String jsonOutput = c.getView("processed_data", "scenario/scenario4").toString();
		System.out.println(c.getView("processed_data", "scenario/scenario4").size());
		System.out.println("***" + jsonOutput);



		CrimeList cl2 = new CrimeList();
		ArrayList<JsonObject> res2 = (ArrayList<JsonObject>) c.getView("instagram", "scenario/scenario4");
		System.out.println("^^^" + res2.toString());
		for (int index = 0; index < res2.size(); index++) {
			String loc = res2.get(index).get("key").getAsJsonArray().get(0).getAsString();
			String sentiment = res2.get(index).get("key").getAsJsonArray().get(1).getAsString();
			int value = res2.get(index).get("value").getAsInt();
			cl2.addElement(loc, value);
		}
		cl2.recordData("s4/ins");
	}
}
