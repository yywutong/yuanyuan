<html>
  <head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
    <meta name='viewport' content='width=device-width, initial-scale=1.0' />
  </head>
  <body style='background-color:#f2f3f2;'>
    <br>
    <table cellpadding='0' cellspacing='0' border='0' id='backgroundTable' width='100%' style='background-color:#f2f3f2;'>
      <tr>
        <td>
          <table cellpadding='0' cellspacing='0' border='0' align='center' width='1000' style='background-color:#ffffff;'>
            <tr>
              <td width='1000' valign='top' style='background-color:#00b5c8'>
                <table cellpadding='0' cellspacing='0' border='0' align='center' width='800'>
                  <tr>
                    <td width='800' valign='middle'>
                      <h1 style='font-family: arial; font-size: 17px; text-align: center;color: #ffffff;'>{{ summary_str | safe }}</h1>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td width='1000' valign='top'>
                <p>&nbsp;</p>
              </td>
            </tr>
            <tr>
              <td width='1000' valign='top'>
                <table cellpadding='0' cellspacing='0' border='0' align='center' width='800'>
                  <tr>
                    <td width='800' valign='top'>
                      <table id='t01' width='800'>
                        <tr bgcolor='#f58500' align='center'>
                          <th>Key</th>
                          <th>Value</th>
                        </tr>
                        {% if data -%}
                        {% for key, value in data.items() -%}
                        <tr bgcolor="#f2f3f2" align="center">
                        <td><font color="blue">{{ key |safe }}</font></td>
                        <td><font color="red">{{ value |safe }}</font></td>
                        </tr>
                        {%- endfor %}
                        {%- endif %}
                      </table>
                      <p style='font-size:13px; font-family:arial; color:#00b5c8; line-height: 18px; text-align:center;'></p>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td>
                <p>&nbsp;</p>
              </td>
            </tr>
            <tr>
              <td width='1000' valign='top' style='background-color:#00b5c8'>
                <table cellpadding='0' cellspacing='0' border='0' align='center' width='800'>
                  <tr>
                    <td width='200' valign='top' align='middle'>
                      <a href='https://www.sensetime.com/cn'>
                        <img src='https://static.sensetime.com/images/logo.png' alt='' width='85' style='width:85px;'>
                        </a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <!-- End example table -->
          </td>
        </tr>
      </table>
      <!-- End of wrapper table -->
    </body>
  </html>
