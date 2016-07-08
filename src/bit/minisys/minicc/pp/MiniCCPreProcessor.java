package bit.minisys.minicc.pp;
/** 
* @author ze01 E-mail: zhulifei@riseup.net
* @version 创建时间：2016年5月16日 上午12:28:54 
* 类说明 
*/
import java.io.PrintStream;

public class MiniCCPreProcessor implements IMiniCCPreProcessor {
	public void run(String iFile, String oFile) {
		PreProcessor pp = new PreProcessor(iFile);
		pp.preProcess(oFile);
		System.out.println("1. PreProcess finished!");
	}
}
