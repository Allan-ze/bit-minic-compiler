import java.io.IOException;

import org.python.util.PythonInterpreter;

/** 
* @author ze01 E-mail: zhulifei@riseup.net
* @version ����ʱ�䣺2016��5��15�� ����12:55:31 
* ��˵�� 
*/
public class Jpython {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
        //�������  
        String[] args2 = {"arg1","arg2"};  
        //���ò���  
        PythonInterpreter.initialize(null, null, args2);
        PythonInterpreter interpreter = new PythonInterpreter();
        interpreter.execfile("input.py");
        try {
			Runtime.getRuntime().exec("python runtime.py 1 2");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
