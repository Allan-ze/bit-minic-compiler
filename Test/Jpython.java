import java.io.IOException;

import org.python.util.PythonInterpreter;

/** 
* @author ze01 E-mail: zhulifei@riseup.net
* @version 创建时间：2016年5月15日 下午12:55:31 
* 类说明 
*/
public class Jpython {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
        //定义参数  
        String[] args2 = {"arg1","arg2"};  
        //设置参数  
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
