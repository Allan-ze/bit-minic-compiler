package bit.minisys.minicc.pp;
/** 
* @author ze01 E-mail: zhulifei@riseup.net
* @version ����ʱ�䣺2016��5��16�� ����12:28:54 
* ��˵�� 
*/
import java.io.PrintStream;

public class MiniCCPreProcessor implements IMiniCCPreProcessor {
	public void run(String iFile, String oFile) {
		PreProcessor pp = new PreProcessor(iFile);
		pp.preProcess(oFile);
		System.out.println("1. PreProcess finished!");
	}
}
