/**
 *  Xiaolu Zhang 886161
 *  Jianbo Ma 807590
 *  Hongyi Lin 838776
 *  Xiaoyu Wang 799778
 *  Shalitha Weerakoon Karunatilleke 822379
 *  COMP90024 Cluster and Cloud Computing
 *  Social Media Analytics on Melbourne & Sydney
 */

package com.ccc.spring.model;

import java.util.ArrayList;

import com.ccc.spring.dao.WriteJsonFile;

public class CrimeList {
	ArrayList<Crime> list = new ArrayList<Crime>();
	
	public void addElement(String location, int value) {
		Integer index = hasElement(location);
		if(index == null) {
			list.add(new Crime(location));
			index = list.size()-1;
		}
		Crime c = list.get(index);
		c.value = value;
	}
	
	public Integer hasElement(String location) {
		for (Integer index = 0; index < list.size(); index++) {
			if (list.get(index).location.equals(location)) {
				return index;
			}
		}
		return null;
	}
	
	public void recordData(String path) {
		String output = "{\n" + 
				"	\"list\": [\n";
		String middle="";
		for (int index = 0; index < list.size()-1;index++) {
			middle +=  				"		{\n" + 
					"			\"department\": \""+list.get(index).location+"\",\n" + 
					"			\"num\": "+list.get(index).value+"\n" + 
					"		},\n"; 
		}
		String end = 				"		{\n" + 
				"			\"department\": \""+list.get(list.size()-1).location+"\",\n" + 
				"			\"num\": "+list.get(list.size()-1).value+"\n" + 
				"		}\n" + 
				"	]\n" + 
				"}";
		
		output = output +middle +end;
		
		WriteJsonFile.WriteConfigJson(output, "s3/"+path+"/" + "piechart.json");
	}
}
