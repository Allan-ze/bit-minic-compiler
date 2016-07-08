package bit.minisys.minicc.pp;
/** 
* @author ze01 E-mail: zhulifei@riseup.net
* @version 创建时间：2016年5月16日 上午12:26:55 
* 类说明 
*/

import bit.minisys.minicc.util.MiniCCUtil;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

public class PreProcessor {
	String path;

	public PreProcessor(String filePath) {
		this.path = filePath;
	}

	public void preProcess(String output) {
		if (!(MiniCCUtil.checkFile(this.path))) {
			return;
		}
		String processed = "";
		File file = new File(this.path);
		try {
			BufferedReader reader = new BufferedReader(new FileReader(file));
			String line = "";
			while ((line = reader.readLine()) != null) {
				line = line.replace("\r\n", "");

				int start = line.indexOf("//");
				if (start == 0) {
					continue;
				}
				if (start > 0) {
					line = line.substring(0, start);
				}

				start = line.indexOf("/*");
				int end = line.indexOf("*/");
				if ((start >= 0) && (end >= 0) && (end - start >= 2)) {
					line = line.substring(0, start);
				}

				processed = processed + line;
			}
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		MiniCCUtil.createAndWriteFile(output, processed);
	}
}
