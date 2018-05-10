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

public class Crime {
	public String location;
	public int value;
	
	public Crime(String location) {
		this.location = location;
		this.value = 0;
	}
}
