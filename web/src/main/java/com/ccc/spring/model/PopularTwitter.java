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

import com.ccc.spring.dao.WriteJsonFile;

public class PopularTwitter {
	public int positive;
	public int negative;
	public int neutral;
	
	public void recordData() {
		String output = "{\n" + 
				"	\"list\": [\n" + 
				"		{\n" + 
				"			\"department\": \"positive\",\n" + 
				"			\"num\": "+this.positive+"\n" + 
				"		},\n" + 
				"		{\n" + 
				"			\"department\": \"negative\",\n" + 
				"			\"num\": "+this.negative+"\n" + 
				"		},\n" + 
				"		{\n" + 
				"			\"department\": \"neutral\",\n" + 
				"			\"num\": "+this.neutral+"\n" + 
				"		}\n" + 
				"	]\n" + 
				"}";
		WriteJsonFile.WriteConfigJson(output,"s5/piechart.json");
	}
}
