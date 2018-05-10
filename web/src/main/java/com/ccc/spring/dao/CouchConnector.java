/**
 *  Xiaolu Zhang 886161
 *  Jianbo Ma 807590
 *  Hongyi Lin 838776
 *  Xiaoyu Wang 799778
 *  Shalitha Weerakoon Karunatilleke 822379
 *  COMP90024 Cluster and Cloud Computing
 *  Social Media Analytics on Melbourne & Sydney
 */

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
