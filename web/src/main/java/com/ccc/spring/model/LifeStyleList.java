package com.ccc.spring.model;

import java.util.ArrayList;

import com.ccc.spring.dao.WriteJsonFile;

public class LifeStyleList {
	public ArrayList<LifeStyle> lifeStyleList = new ArrayList<LifeStyle>();

	public LifeStyleList() {
		this.lifeStyleList.add(new LifeStyle("education"));
		this.lifeStyleList.add(new LifeStyle("entertainment"));
		this.lifeStyleList.add(new LifeStyle("food"));
		this.lifeStyleList.add(new LifeStyle("living"));
		this.lifeStyleList.add(new LifeStyle("medical"));
		this.lifeStyleList.add(new LifeStyle("shopping"));
		this.lifeStyleList.add(new LifeStyle("sports"));
		this.lifeStyleList.add(new LifeStyle("traffic"));
		this.lifeStyleList.add(new LifeStyle("travel"));
	}

	public void recordData(String path) {
		for (int index = 0; index < lifeStyleList.size(); index++) {
			LifeStyle ls = lifeStyleList.get(index);
			ls.getTotal();
			String output = "{\"data\":[" + ls.positive + "," + ls.negative + "," + ls.neutral + "]}";
			WriteJsonFile.WriteConfigJson(output, "s1/"+path+"/" + ls.name + ".json");
		}
		String output = "{\n" + 
				"	\"list\": [\n" + 
				"		{\n" + 
				"			\"department\": \"education\",\n" + 
				"			\"num\": "+lifeStyleList.get(0).total+"\n" + 
				"		},\n" + 
				"		{\n" + 
				"			\"department\": \"entertainment\",\n" + 
				"			\"num\": "+lifeStyleList.get(1).total+"\n" + 
				"		},\n" + 
				"		{\n" + 
				"			\"department\": \"food\",\n" + 
				"			\"num\": "+lifeStyleList.get(2).total+"\n" + 
				"		},\n" + 
				"		{\n" + 
				"			\"department\": \"living\",\n" + 
				"			\"num\": "+lifeStyleList.get(3).total+"\n" + 
				"		},\n" + 
				"		{\n" + 
				"			\"department\": \"medical\",\n" + 
				"			\"num\": "+lifeStyleList.get(4).total+"\n" + 
				"		},\n" + 
				"		{\n" + 
				"			\"department\": \"shopping\",\n" + 
				"			\"num\": "+lifeStyleList.get(5).total+"\n" + 
				"		},\n" + 
				"		{\n" + 
				"			\"department\": \"sports\",\n" + 
				"			\"num\": "+lifeStyleList.get(6).total+"\n" + 
				"		},\n" + 
				"		{\n" + 
				"			\"department\": \"traffic\",\n" + 
				"			\"num\": "+lifeStyleList.get(7).total+"\n" + 
				"		},\n" + 
				"		{\n" + 
				"			\"department\": \"travel\",\n" + 
				"			\"num\": "+lifeStyleList.get(8).total+"\n" + 
				"		}\n" + 
				"	]\n" + 
				"}";
		WriteJsonFile.WriteConfigJson(output, "s1/"+path+"/" + "piechart.json");
	}

}
