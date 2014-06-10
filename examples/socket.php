<?php
error_reporting(E_ALL);

/* Allow the script to hang around waiting for connections. */
set_time_limit(0);

/* Turn on implicit output flushing so we see what we're getting
 * as it comes in. */
ob_implicit_flush();

$address = '127.0.0.1';
$port = 10010;
$respuesta = '';
$arr_usu = 0;
$timeout = 20; //a los 20 segundos te "desloguea"
$socket_hub = '';

if (($sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP)) === false) {
    echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
}

if (socket_bind($sock, $address, $port) === false) {
    echo "socket_bind() failed: reason: " . socket_strerror(socket_last_error($sock)) . "\n";
}

//acepto hasta 5 en cola (6 en total, el que estoy sirviendo y 5 en cola)
if (socket_listen($sock, 5) === false) {
    echo "socket_listen() failed: reason: " . socket_strerror(socket_last_error($sock)) . "\n";
}

do {
    if (($msgsock = socket_accept($sock)) === false) {
        echo "socket_accept() failed: reason: " . socket_strerror(socket_last_error($sock)) . "\n";
        break;
    }
    /* Send instructions. */
//    $msg = "\nWelcome to the PHP Test Server. \n" .
//        "To quit, type 'quit'. To shut down the server type 'shutdown'.\n";
//    socket_write($msgsock, $msg, strlen($msg));

    do {
    	//si no puedo leer el socket, salgo y corto todo!, debría mandar un email aca!
        if (false === ($buf = socket_read($msgsock, 2048, PHP_NORMAL_READ))) {
            echo "socket_read() failed: reason: " . socket_strerror(socket_last_error($msgsock)) . "\n";
            break 2;
        }
        if (!$buf = trim($buf)) {
            continue;
        }
        if ($buf == 'quit') {
            break;
        }
        $respuesta = "";
        $tipo_transaccion = obtenerTipoTransaccion($buf);
        
        switch ($tipo_transaccion){
	        case "0800":
	        	//es un requerimiento de conexión, puede ser login, logout o echo
	        	$tipo_login = parsearInputpaConexion($buf);
	        	switch ($tipo_login){
	        		case "001":
	        			//logon. logueo al cliente y devuelvo respuesta
	        			$arr_usu = time();
	        			//$respuesta = "es un login";
	        			$respuesta = armarRespuesta($buf, 1, $tipo_login, "");
	        		break;
	        		
	        		case "002":
		        		//logout. deslogueo al cliente y devuelvo respuesta
		        		$arr_usu = 0;
		        		//$respuesta = "es un logout";
		        		$respuesta = armarRespuesta($buf, 1, $tipo_login, "");
	        		break;
	        		
	        		case "301":
	        			//echo. reinicio tiempo inactividad de ese cliente
	        			$arr_usu = time();
	        			//$respuesta = "es un echo";
	        			$respuesta = armarRespuesta($buf, 1, $tipo_login, "");
	        		break;
	        		
	        		default:
			        	//codigo de operacion no valido
	    		    	$respuesta = "Conexion - NMIC(S-070) invalido";
	        		break;
	        	}
	        break;

	        case "0200":
	        	//es un requerimiento de recarga
	        	$usuario_logueado = validaUsuarioLogueado($arr_usu, $timeout);
	        	if (1){ //($usuario_logueado){
                    /*
		        	$arr_usu = time();
		        	$parametros_entrada = array();
		        	$parametros_respuesta = array();
		        	$parametros_entrada = extraerParametrosRecarga($buf);
		        	//echo "telefono: " .$parametros_entrada['telefono']."\n";
		        	//echo "monto: " .$parametros_entrada['monto']."\n";
		        	$parametros_respuesta = enviarTransaccionHub($parametros_entrada['telefono'],$parametros_entrada['monto']);
		        	//si no hubo una respuesta satisfactoria, el ticket lo pongo en 0
		        	if($parametros_respuesta['codrespuestaOut'] != 'O'){
		        		$parametros_respuesta['importeOut'] = 0;
		        		if($parametros_respuesta['codrespuestaOut'] == 'E' && ($parametros_respuesta['descripcionOut'] == '009' || $parametros_respuesta['descripcionOut'] == '025')){
		        			//linea mal cargada: 82
		        			$resultado_transaccion = "82";
		        		}
		        		else{
		        			//error interno: 90. cualquier otro error que no sea el 009, incluidos los del HUB
		        			$resultado_transaccion = "90";
		        		}
		        	}
		        	else{
		        		//respuesta ok: 00. la transaccion se proceso bien
		        		$resultado_transaccion = "00";
		        	}
	        	}
	        	else{
	        		echo "usuairo deslogueado\n";
                */
                    print "paso de largo";
	        	}
                // Clavado por mi
           		$resultado_transaccion = "00";
                $parametros_respuesta = Array();
                $parametros_respuesta['importeOut'] = 0;
                // Fuin clavado por mi

		        $respuesta = armarRespuesta($buf, 2, $parametros_respuesta['importeOut'], $resultado_transaccion);
	        break;
	        
	        case "0420":
	        case "0421":
	        	//es un reverso de recarga. no esta soportado
	        	$respuesta = "es un reverso";
	        break;
	        
	        default:
	        	//codigo de operacion no valido
	        	$respuesta = "Operacion - MTI (C-003) invalido";
	        break;
        }
        
        //mira que bueno esto!!!! sale de los 2 while!!!!
        if ($buf == 'shutdown') {
        	socket_write($msgsock, "Hasta la vista...baby", 21);
            socket_close($msgsock);
            break 2;
        }
        $respuesta = $respuesta."\n";
        socket_write($msgsock, $respuesta, strlen($respuesta));
        //echo "recibido: ".$buf ."\n";
        //echo "devuelto: ".$respuesta ."\n";
    } while (true);
    socket_close($msgsock);
} while (true);

socket_close($sock);


function obtenerTipoTransaccion($stream_buffered){
	//saco los 4 caracteres que le siguen al caracter 13
	$tipotran = substr($stream_buffered, 12, 4);
	//echo "tipotransaccion: " . $tipotran."\n";
	return $tipotran;
}

function parsearInputpaConexion($stream_buffered){
	//saco los ultimos 3 caracteres de los ultimos 4 de la cadena: AAAAAAA....BBBA
	$tipotran = substr($stream_buffered, strlen($stream_buffered)-4, 3);
	//echo "tipologin: " . $tipotran."\n";
	return $tipotran;
}

function parsearInputpaLogin($stream_buffered){
	//saco los ultimos 3 caracteres de los ultimos 4 de la cadena: AAAAAAA....BBBA
	$tipotran = substr($stream_buffered, strlen($stream_buffered)-4, 3);
	return $tipotran;
}

function armarRespuesta($stream_buffered, $tipo, $accion, $detalle){
	$nueva_respuesta = '';
	switch($tipo){
	case 1:
		/*respuesta a un login 
		cambia el ultimo caracter del C-002 a 5,
		cambia c-003 a 0810
		cambia c-004 a 8220000002000000
		cambia p-001 a 0400000000000000
		se agrega p-039 en el caracter de 64 la respuesta. los valores son 00 aprobado, 05 denegado y 91 abajo
		*/
		$cadena1 = substr($stream_buffered, 0, 11); //los primeros 11 caracteres
		$cadena2 = substr($stream_buffered, 48, 16); //los datos de P-007 y P-011
		$cadena3 = substr($stream_buffered, strlen($stream_buffered)-1, 1); //el terminador
		
		$nueva_respuesta = $cadena1 . "5081082200000020000000400000000000000" . $cadena2 . "00" . $accion . $cadena3;
	break;
	
	case 2:
		/*respuesta a una recarga
		cambia c-003 a 0210
		cambia c-004 a B038800008808018
		cambia p-001 a 0000000000000004
		se agrega p-039 en el caracter de 98 la respuesta. los valores son 00 aprobado, 82 linea invalida y 90 error interno. esto viene en $detalle
		hay algo en s-126: 99-114 numero de autorizacion y 115-144 numero de autorizacion : que sera esto? asumo que es el id de transaccion de claro 
		*/

		$cadena1 = substr($stream_buffered, 0, 12); //los primeros 12 caracteres
		$cadena2 = substr($stream_buffered, 48, 50); //todo lo que hay desde p-003 hasta p-037 inclusive
		$cadena3 = substr($stream_buffered, 98, 150); //todo lo que hay luego de p-037 hasta la posicion 99 de S-126
		$cadena4 = substr($stream_buffered, 294, 88); //todo lo que hay luego de la posicion 145 de S-126 hasta el terminador inclusive
        
        echo "accion:".$accion;
        echo "detalle".$detalle;
        echo "cadena1:".$cadena1;
        echo "cadena2:".$cadena2;
        echo "cadena3:".$cadena3;
        echo "cadena4:".$cadena4;


		$accion1 = str_pad($accion, 16);
		$accion2 = str_pad($accion, 30);
		$nueva_respuesta = $cadena1 . "0210B0388000088080180000000000000004" . $cadena2 . $detalle . $cadena3 . $accion1 . $accion2 . $cadena4;
	break;
	}

	return $nueva_respuesta;
}

function extraerParametrosRecarga($stream_buffered){
/*saco el telefono y el monto a recargar
 * el telefono esta en S-126, en la posicion 80-98:	Cliente. pero este dato es variable
 * el monto esta en P-004, con 2 decimales. esto es la posicion 55 a la 67 del stream_buffered 
*/
	$monto = substr($stream_buffered, 55, 11);
	$monto = intval($monto) / 100; //convierto a entero y saco los decimales
	$telefono = substr($stream_buffered, 229, 19); //los caracteres que corresponden al telefono dentro de S-126. estan padding con espacios en blanco
	$telefono = trim($telefono, " "); //saco los espacios en blanco
	//echo $monto . "-" . $telefono;
	$arr = array('telefono' => $telefono, 'monto' => $monto);
	return $arr; 
}


function enviarTransaccionHub($telefono, $monto){
/* armo la llamada al hub y guardo la respuesta del HUB en un array para dev */

	$fechalote = armar_fecha_para_lote();
	if (strlen($monto) == 2)
		$monto = "0".$monto;
		
	$monto = "VVS". $monto;	
	$lote = $telefono.$fechalote;
	
	//genero el verificador
	$verificador = generar_hash($lote, $telefono, 27, $monto, "1234", "clavebanelco");
	
	//armo el xml
	$xml = armar_xml($lote, $telefono, 27, $monto, "1234", $verificador, "\r\n");
	
	//envio la transaccion
	$response_xml = enviar_request_hub($xml);

	//parseo la respuesta y la devuelvo
	return parsear_response_hub($response_xml);
}


function armar_fecha_para_lote(){
	$fecha = getdate();
	$mes = $fecha["mon"];
	$dia = $fecha["mday"];
	$hora = $fecha["hours"];
	$minuto = $fecha["minutes"];
	$segundo = $fecha["seconds"];
	
	if(strlen($mes)==1) 
		$mes = "0".$mes;
		
	if(strlen($dia)==1) 
		$dia = "0".$dia;
		
	if(strlen($hora)==1) 
		$hora = "0".$hora;
	
	if(strlen($minuto)==1) 
		$minuto = "0".$minuto;
		
	if(strlen($segundo)==1) 
		$segundo = "0".$segundo;
		
	$pfechalote = $fecha["year"].$mes.$dia.$hora.$minuto.$segundo;
	return $pfechalote;
}

function generar_hash($plote, $ptelefono, $pentidad, $pmonto, $ppos, $pclavecliente){
	$cadena_a_hashear = $plote.$ptelefono.$pmonto."S".$pentidad.$ppos.$pclavecliente;
	$pverificador = sha1($cadena_a_hashear);
	
	return $pverificador;
}

function armar_xml($plote, $pfono, $pentidad, $pmonto, $ppos, $pverificador, $peol){
	$pxml = '<?xml version = "1.0" encoding = "UTF-8"?>'.$peol.
			'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">'.$peol.
			'<SOAP-ENV:Body>'.$peol.
			'<ns1:pinvirtualtrans xmlns:ns1="pinvirtualService" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'.$peol.
			'<lote xsi:type="xsd:string">'.$plote.'</lote>'.$peol.
			'<bill xsi:type="xsd:string">'.$pfono.'</bill>'.$peol.
			'<codtarjeta xsi:type="xsd:string">'.$pmonto.'</codtarjeta>'.$peol.
			'<codoperacion xsi:type="xsd:string">S</codoperacion>'.$peol.
			'<codentidad xsi:type="xsd:string">'.$pentidad.'</codentidad>'.$peol.
			'<pos xsi:type="xsd:string">'.$ppos.'</pos>'.$peol.
			'<verificador xsi:type="xsd:string">'.$pverificador.'</verificador>'.$peol.
			'</ns1:pinvirtualtrans>'.$peol.
			'</SOAP-ENV:Body>'.$peol.
			'</SOAP-ENV:Envelope>';
	
	return $pxml;
}

function parsear_response_hub($pxml)
{
	$request = __simplexml_load_string($pxml);
	//echo "REQUEST " . $request . "\n";
	$rq = array();
	try{
		$rq['codrespuestaOut'] = (string) $request->SOAPENV_Body->ns1pinvirtualtransResponse->return->codrespuestaOut;
		$rq['descripcionOut']  = (string) $request->SOAPENV_Body->ns1pinvirtualtransResponse->return->descripcionOut;
		$rq['importeOut']      = (string) $request->SOAPENV_Body->ns1pinvirtualtransResponse->return->importeOut;
		$rq['importetarjOut']  = (string) $request->SOAPENV_Body->ns1pinvirtualtransResponse->return->importetarjOut;
		$rq['mensajeOut']      = (string)$request->SOAPENV_Body->ns1pinvirtualtransResponse->return->mensajeOut;	
	}
	catch(Exception $e){
		$rq['codrespuestaOut'] = (string) $request->SOAPENV_Body->ns1pinvirtualtransResponse->return->codrespuestaOut;
		$rq['descripcionOut']  = (string) $request->SOAPENV_Body->ns1pinvirtualtransResponse->return->descripcionOut;
		$rq['importeOut']      = 0;
		$rq['importetarjOut']  = 0;
		$rq['mensajeOut']      = (string)$request->SOAPENV_Body->ns1pinvirtualtransResponse->return->mensajeOut;
	}
	return $rq;
}

function __simplexml_load_string($pxml2)
{
	$pxml2 = str_replace('SOAP-ENV:','SOAPENV_',$pxml2);
	$pxml2 = preg_replace('|<([/\w]+)(:)|m','<$1' ,$pxml2);  
	$pxml2 = preg_replace('|(\w+)(:)(\w+=\")|m','$1$3',$pxml2);  
	$result = simplexml_load_string($pxml2);
	return $result;
}

function enviar_request_hub($pxml){	
	
	$length = strlen($pxml);
	$port = 80; 
	$host = 'pruebas.hubvirtual.com.ar'; //
	$path = '/app/servicio.php'; //
	$out = '';
//	echo $pxml ."\n";
	$sockethub = fsockopen($host, 80, $errno, $errstr, 10);
	fputs($sockethub, "POST $path HTTP/1.0\r\n");
	fputs($sockethub, "Host: $host \r\n");
	fputs($sockethub, "Content-Type: text/html\r\n");
	fputs($sockethub, "Content-Length: $length\r\n");
	fputs($sockethub, "\r\n");
	fputs($sockethub, $pxml);
	while (!feof($sockethub)) {
	   $out .= fread($sockethub, 1024);
	}
	fclose($sockethub);
	$sockethub = '';
	//echo "respuesta sin filtrar: " . $out."\n\n";
	
	//saco los headers HTML de la respuesta
	$out = substr($out, strpos($out, '<'));
	//echo "respuesta filtrada:" . $out."\n\n";
	
	return $out; //es un string lo que devuelvo aca
}

function validaUsuarioLogueado($last_tran, $time_out){
	$diferencia = time() - $last_tran;
	if($diferencia > $time_out)
		return false;
	else
		return true;
}
?>
