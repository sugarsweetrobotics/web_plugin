
import 'dart:html' as html;
import 'package:logging/logging.dart';
import 'package:polymer/polymer.dart';

import 'package:wasanbon_elements/wasanbon_toolbar.dart';
import 'setting_tool.dart';

import 'package:settingmanager/settingmanager.dart' as manager;
import 'package:wasanbon_xmlrpc/wasanbon_xmlrpc.dart' as wasanbon;
import 'package:http/browser_client.dart' as client;

/// Silence analyzer [MyElement]
main() async {

  print(Uri.base.host);
  print(Uri.base.port);
  print(Uri.base.queryParameters);

  manager.rpc = new wasanbon.WasanbonRPC(url: Uri.base.queryParameters['wasanbon'] == null ? 'http://${Uri.base.host}:${Uri.base.port}/RPC' : 'http://${Uri.base.queryParameters['wasanbon']}/RPC', client: new client.BrowserClient());

  Logger.root.level = Level.ALL;
  manager.rpc.onRecordListen((LogRecord rec) {
    print('${rec.level.name}: ${rec.time}: ${rec.message}');
  });

  await initPolymer();
}
