package bit.minisys.minicc;

public class MiniCCCfg {
	// input and output for preprocessor
	public static String MINICC_PP_INPUT_EXT = ".c";//CԴ����
	public static String MINICC_PP_OUTPUT_EXT = ".pp";
	// input and output for scanner
	public static String MINICC_SCANNER_INPUT_EXT = ".pp";//Ԥ�������C����
	public static String MINICC_SCANNER_OUTPUT_EXT = ".l";
	// input and output for parser
	public static String MINICC_PARSER_INPUT_EXT = ".l";//�ʷ�������������ַ���
	public static String MINICC_PARSER_OUTPUT_EXT = ".y";
	// input and output for codegen
	public static String MINICC_CODEGEN_INPUT_EXT = ".y";//�м����
	public static String MINICC_CODEGEN_OUTPUT_EXT = ".s";
	// input and output for optimizer
	public static String MINICC_OPT1_INPUT_EXT = ".s";//Ŀ�����(MIPS������)
	public static String MINICC_OPT1_OUTPUT_EXT = ".s1";
	// input and output for assembler
	public static String MINICC_ASSEMBLER_INPUT_EXT = ".s1";//�Ż����Ŀ�����
	public static String MINICC_ASSEMBLER_OUTPUT_EXT = ".bin";
	// input and output for simulator
	public static String MINICC_SIMULATOR_INPUT_EXT = ".bin";//�����ļ�
}
