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

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class WriteJsonFile {
	public static void WriteConfigJson(String args, String path) {
		// String src = "./src/main/webapp/data/s1/test.json";
		String src = "./src/main/webapp/data/" + path;
		System.out.println(src);
		File file = new File(src);

		if (!file.getParentFile().exists()) {
			file.getParentFile().mkdirs();
		}
		try {
			file.delete();
			file.createNewFile();
		} catch (IOException e) {
			e.printStackTrace();
		}

		try {
			FileWriter fw = new FileWriter(file, true);
			fw.write(args);
			fw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}