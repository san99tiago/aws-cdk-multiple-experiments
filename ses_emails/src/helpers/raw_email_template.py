# I used "unlayer.com" to generate the email template (just for the PoC)
# Note: It's required to update the images from the local path, to the target URLs


class HTMLCustomTemplate:
    """
    Class that loads an HTML template with custom variables for customization.
    """

    def __init__(self, s3_url: str) -> None:
        """ ""
        :params s3_url (str): S3 bucket URL to be used as a prefix for images.
        """
        # Example with just one param, but could have as many params as needed
        self.s3_url = s3_url

    def generate_template(self) -> str:
        """
        Method to generate the HTML template from input variables.
        """

        return f"""
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html
        xmlns="http://www.w3.org/1999/xhtml"
        xmlns:v="urn:schemas-microsoft-com:vml"
        xmlns:o="urn:schemas-microsoft-com:office:office"
        >
        <head>
            <!--[if gte mso 9]>
            <xml>
                <o:OfficeDocumentSettings>
                <o:AllowPNG />
                <o:PixelsPerInch>96</o:PixelsPerInch>
                </o:OfficeDocumentSettings>
            </xml>
            <![endif]-->
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <meta name="x-apple-disable-message-reformatting" />
            <!--[if !mso]><!-->
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <!--<![endif]-->
            <title></title>

            <style type="text/css">
            @media only screen and (min-width: 620px) {{
                .u-row {{
                width: 600px !important;
                }}
                .u-row .u-col {{
                vertical-align: top;
                }}

                .u-row .u-col-25 {{
                width: 150px !important;
                }}

                .u-row .u-col-50 {{
                width: 300px !important;
                }}

                .u-row .u-col-100 {{
                width: 600px !important;
                }}
            }}

            @media (max-width: 620px) {{
                .u-row-container {{
                max-width: 100% !important;
                padding-left: 0px !important;
                padding-right: 0px !important;
                }}
                .u-row .u-col {{
                min-width: 320px !important;
                max-width: 100% !important;
                display: block !important;
                }}
                .u-row {{
                width: 100% !important;
                }}
                .u-col {{
                width: 100% !important;
                }}
                .u-col > div {{
                margin: 0 auto;
                }}
            }}
            body {{
                margin: 0;
                padding: 0;
            }}

            table,
            tr,
            td {{
                vertical-align: top;
                border-collapse: collapse;
            }}

            p {{
                margin: 0;
            }}

            .ie-container table,
            .mso-container table {{
                table-layout: fixed;
            }}

            * {{
                line-height: inherit;
            }}

            a[x-apple-data-detectors="true"] {{
                color: inherit !important;
                text-decoration: none !important;
            }}

            @media (max-width: 480px) {{
                .hide-mobile {{
                max-height: 0px;
                overflow: hidden;
                display: none !important;
                }}
            }}

            table,
            td {{
                color: #000000;
            }}
            #u_body a {{
                color: #0000ee;
                text-decoration: underline;
            }}
            #u_content_text_13 a {{
                color: #ec19ae;
            }}
            @media (max-width: 480px) {{
                #u_content_text_1 .v-container-padding-padding {{
                padding: 10px 10px 40px !important;
                }}
                #u_content_text_1 .v-font-size {{
                font-size: 37px !important;
                }}
                #u_content_text_1 .v-line-height {{
                line-height: 100% !important;
                }}
                #u_content_text_2 .v-container-padding-padding {{
                padding: 40px 10px 0px !important;
                }}
                #u_content_text_2 .v-font-size {{
                font-size: 26px !important;
                }}
                #u_content_text_2 .v-line-height {{
                line-height: 120% !important;
                }}
                #u_content_text_4 .v-container-padding-padding {{
                padding: 5px 10px 10px !important;
                }}
                #u_content_text_4 .v-font-size {{
                font-size: 14px !important;
                }}
                #u_content_text_4 .v-line-height {{
                line-height: 130% !important;
                }}
                #u_content_button_5 .v-container-padding-padding {{
                padding: 10px 10px 0px !important;
                }}
                #u_content_button_5 .v-text-align {{
                text-align: center !important;
                }}
                #u_content_button_1 .v-container-padding-padding {{
                padding: 10px 10px 40px !important;
                }}
                #u_content_button_1 .v-text-align {{
                text-align: center !important;
                }}
                #u_content_image_3 .v-container-padding-padding {{
                padding: 0px 10px 10px !important;
                }}
                #u_content_heading_6 .v-container-padding-padding {{
                padding: 10px 10px 0px !important;
                }}
                #u_content_heading_6 .v-text-align {{
                text-align: center !important;
                }}
                #u_content_text_6 .v-text-align {{
                text-align: center !important;
                }}
                #u_content_text_13 .v-container-padding-padding {{
                padding: 5px 10px 40px !important;
                }}
                #u_content_text_13 .v-text-align {{
                text-align: center !important;
                }}
                #u_column_10 .v-col-border {{
                border-top: 0px solid transparent !important;
                border-left: 0px solid transparent !important;
                border-right: 0px solid transparent !important;
                border-bottom: 1px solid #ccc !important;
                }}
                #u_content_image_4 .v-src-width {{
                width: auto !important;
                }}
                #u_content_image_4 .v-src-max-width {{
                max-width: 20% !important;
                }}
                #u_column_11 .v-col-border {{
                border-top: 0px solid transparent !important;
                border-left: 0px solid transparent !important;
                border-right: 0px solid transparent !important;
                border-bottom: 1px solid #ccc !important;
                }}
                #u_content_image_5 .v-src-width {{
                width: auto !important;
                }}
                #u_content_image_5 .v-src-max-width {{
                max-width: 16% !important;
                }}
                #u_column_12 .v-col-border {{
                border-top: 0px solid transparent !important;
                border-left: 0px solid transparent !important;
                border-right: 0px solid transparent !important;
                border-bottom: 1px solid #ccc !important;
                }}
                #u_content_image_6 .v-src-width {{
                width: auto !important;
                }}
                #u_content_image_6 .v-src-max-width {{
                max-width: 21% !important;
                }}
                #u_content_image_7 .v-src-width {{
                width: auto !important;
                }}
                #u_content_image_7 .v-src-max-width {{
                max-width: 17% !important;
                }}
                #u_content_text_15 .v-container-padding-padding {{
                padding: 40px 10px 10px !important;
                }}
                #u_content_menu_2 .v-padding {{
                padding: 5px 10px !important;
                }}
            }}
            </style>
        </head>

        <body
            class="clean-body u_body"
            style="
            margin: 0;
            padding: 0;
            -webkit-text-size-adjust: 100%;
            background-color: #e7e7e7;
            color: #000000;
            "
        >
            <!--[if IE]><div class="ie-container"><![endif]-->
            <!--[if mso]><div class="mso-container"><![endif]-->
            <table
            id="u_body"
            style="
                border-collapse: collapse;
                table-layout: fixed;
                border-spacing: 0;
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                vertical-align: top;
                min-width: 320px;
                margin: 0 auto;
                background-color: #e7e7e7;
                width: 100%;
            "
            cellpadding="0"
            cellspacing="0"
            >
            <tbody>
                <tr style="vertical-align: top">
                <td
                    style="
                    word-break: break-word;
                    border-collapse: collapse !important;
                    vertical-align: top;
                    "
                >
                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #e7e7e7;"><![endif]-->

                    <div
                    class="u-row-container"
                    style="padding: 0px; background-color: transparent"
                    >
                    <div
                        class="u-row"
                        style="
                        margin: 0 auto;
                        min-width: 320px;
                        max-width: 600px;
                        overflow-wrap: break-word;
                        word-wrap: break-word;
                        word-break: break-word;
                        background-color: transparent;
                        "
                    >
                        <div
                        style="
                            border-collapse: collapse;
                            display: table;
                            width: 100%;
                            height: 100%;
                            background-color: transparent;
                        "
                        >
                        <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->

                        <!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-border" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]-->
                        <div
                            class="u-col u-col-100"
                            style="
                            max-width: 320px;
                            min-width: 600px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div style="height: 100%; width: 100% !important">
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                "
                            ><!--<![endif]-->
                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                        </div>
                    </div>
                    </div>

                    <div
                    class="u-row-container"
                    style="padding: 0px; background-color: transparent"
                    >
                    <div
                        class="u-row"
                        style="
                        margin: 0 auto;
                        min-width: 320px;
                        max-width: 600px;
                        overflow-wrap: break-word;
                        word-wrap: break-word;
                        word-break: break-word;
                        background-color: transparent;
                        "
                    >
                        <div
                        style="
                            border-collapse: collapse;
                            display: table;
                            width: 100%;
                            height: 100%;
                            background-color: transparent;
                        "
                        >
                        <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->

                        <!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-border" style="background-color: #000000;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                        <div
                            class="u-col u-col-100"
                            style="
                            max-width: 320px;
                            min-width: 600px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div
                            style="
                                background-color: #000000;
                                height: 100%;
                                width: 100% !important;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                            "
                            >
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                                "
                            ><!--<![endif]-->
                                <table
                                id="u_content_text_1"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 10px 10px 60px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            font-size: 48px;
                                            color: #ffffff;
                                            line-height: 120%;
                                            text-align: center;
                                            word-wrap: break-word;
                                        "
                                        >
                                        <p style="line-height: 120%">
                                            <span style="line-height: 57.6px"
                                            ><span style="line-height: 57.6px"
                                                ><span style="line-height: 57.6px"
                                                ><span style="line-height: 57.6px"
                                                    >SAN99TIAGO</span
                                                ></span
                                                ></span
                                            ></span
                                            >
                                        </p>
                                        <p style="line-height: 120%">
                                            <span style="line-height: 57.6px"
                                            ><span style="line-height: 57.6px"
                                                ><span style="line-height: 57.6px"
                                                ><span style="line-height: 57.6px"
                                                    >NEWSLETTER</span
                                                ></span
                                                ></span
                                            ></span
                                            >
                                        </p>
                                        <p style="line-height: 120%">
                                            <span style="line-height: 57.6px"
                                            ><span style="line-height: 57.6px"
                                                ><span style="color: #ec19ae"
                                                ><strong>COCO, WE WILL</strong></span
                                                ></span
                                            ></span
                                            >
                                        </p>
                                        <p style="line-height: 120%">
                                            <span style="line-height: 57.6px"
                                            ><span style="line-height: 57.6px"
                                                ><span style="color: #ec19ae"
                                                ><strong
                                                    ><span
                                                    style="
                                                        color: #ec19ae;
                                                        line-height: 57.6px;
                                                    "
                                                    ><strong>MISS YOU!</strong></span
                                                    ></strong
                                                ></span
                                                ><br /></span
                                            ></span>
                                        </p>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 0px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <table
                                        width="100%"
                                        cellpadding="0"
                                        cellspacing="0"
                                        border="0"
                                        >
                                        <tr>
                                            <td
                                            class="v-text-align"
                                            style="
                                                padding-right: 0px;
                                                padding-left: 0px;
                                            "
                                            align="center"
                                            >
                                            <img
                                                align="center"
                                                border="0"
                                                src="{self.s3_url}/ses_images/image-10.png"
                                                alt="image"
                                                title="image"
                                                style="
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                clear: both;
                                                display: inline-block !important;
                                                border: none;
                                                height: auto;
                                                float: none;
                                                width: 100%;
                                                max-width: 600px;
                                                "
                                                width="600"
                                                class="v-src-width v-src-max-width"
                                            />
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                        </div>
                    </div>
                    </div>

                    <div
                    class="u-row-container"
                    style="padding: 0px; background-color: transparent"
                    >
                    <div
                        class="u-row"
                        style="
                        margin: 0 auto;
                        min-width: 320px;
                        max-width: 600px;
                        overflow-wrap: break-word;
                        word-wrap: break-word;
                        word-break: break-word;
                        background-color: transparent;
                        "
                    >
                        <div
                        style="
                            border-collapse: collapse;
                            display: table;
                            width: 100%;
                            height: 100%;
                            background-color: transparent;
                        "
                        >
                        <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->

                        <!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-border" style="background-color: #ffffff;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                        <div
                            class="u-col u-col-100"
                            style="
                            max-width: 320px;
                            min-width: 600px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div
                            style="
                                background-color: #ffffff;
                                height: 100%;
                                width: 100% !important;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                            "
                            >
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                                "
                            ><!--<![endif]-->
                                <table
                                id="u_content_text_2"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 60px 10px 0px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            font-size: 41px;
                                            color: #ffffff;
                                            line-height: 120%;
                                            text-align: center;
                                            word-wrap: break-word;
                                        "
                                        >
                                        <p style="line-height: 120%">
                                            <span
                                            style="
                                                color: #000000;
                                                line-height: 49.2px;
                                            "
                                            ><strong>Learn more at:</strong></span
                                            >
                                        </p>
                                        <p style="line-height: 120%">
                                            <a
                                            rel="noopener"
                                            href="https://san99tiago.com"
                                            target="_blank"
                                            ><strong
                                                ><span
                                                style="
                                                    color: #ec19ae;
                                                    line-height: 49.2px;
                                                "
                                                ><span style="line-height: 49.2px"
                                                    ><span style="line-height: 49.2px"
                                                    >san99tiago.com</span
                                                    ></span
                                                ></span
                                                ></strong
                                            ></a
                                            >
                                        </p>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                id="u_content_text_4"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 5px 10px 35px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            font-size: 14px;
                                            line-height: 140%;
                                            text-align: center;
                                            word-wrap: break-word;
                                        "
                                        >
                                        <p style="line-height: 140%">
                                            We hope this email finds you well. This is
                                            one of my sample templates developed on top
                                            of AWS infrastructure with SES and custom
                                            emails in place.
                                        </p>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                        </div>
                    </div>
                    </div>

                    <div
                    class="u-row-container"
                    style="padding: 0px; background-color: transparent"
                    >
                    <div
                        class="u-row"
                        style="
                        margin: 0 auto;
                        min-width: 320px;
                        max-width: 600px;
                        overflow-wrap: break-word;
                        word-wrap: break-word;
                        word-break: break-word;
                        background-color: transparent;
                        "
                    >
                        <div
                        style="
                            border-collapse: collapse;
                            display: table;
                            width: 100%;
                            height: 100%;
                            background-color: transparent;
                        "
                        >
                        <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->

                        <!--[if (mso)|(IE)]><td align="center" width="300" class="v-col-border" style="background-color: #ffffff;width: 300px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                        <div
                            class="u-col u-col-50"
                            style="
                            max-width: 320px;
                            min-width: 300px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div
                            style="
                                background-color: #ffffff;
                                height: 100%;
                                width: 100% !important;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                            "
                            >
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                                "
                            ><!--<![endif]-->
                                <table
                                id="u_content_button_5"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 10px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <!--[if mso
                                        ]><style>
                                            .v-button {{
                                            background: transparent !important;
                                            }}
                                        </style><!
                                        [endif]-->
                                        <div class="v-text-align" align="right">
                                        <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://github.com/san99tiago" style="height:37px; v-text-anchor:middle; width:202px;" arcsize="11%"  stroke="f" fillcolor="#a107f9"><w:anchorlock/><center style="color:#FFFFFF;"><![endif]-->
                                        <a
                                            href="https://github.com/san99tiago"
                                            target="_blank"
                                            class="v-button v-font-size"
                                            style="
                                            box-sizing: border-box;
                                            display: inline-block;
                                            text-decoration: none;
                                            -webkit-text-size-adjust: none;
                                            text-align: center;
                                            color: #ffffff;
                                            background-color: #a107f9;
                                            border-radius: 4px;
                                            -webkit-border-radius: 4px;
                                            -moz-border-radius: 4px;
                                            width: 72%;
                                            max-width: 100%;
                                            overflow-wrap: break-word;
                                            word-break: break-word;
                                            word-wrap: break-word;
                                            mso-border-alt: none;
                                            font-size: 14px;
                                            "
                                        >
                                            <span
                                            class="v-line-height v-padding"
                                            style="
                                                display: block;
                                                padding: 10px 20px;
                                                line-height: 120%;
                                            "
                                            >GitHub</span
                                            >
                                        </a>
                                        <!--[if mso]></center></v:roundrect><![endif]-->
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]><td align="center" width="300" class="v-col-border" style="background-color: #ffffff;width: 300px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                        <div
                            class="u-col u-col-50"
                            style="
                            max-width: 320px;
                            min-width: 300px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div
                            style="
                                background-color: #ffffff;
                                height: 100%;
                                width: 100% !important;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                            "
                            >
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                                "
                            ><!--<![endif]-->
                                <table
                                id="u_content_button_1"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 10px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <!--[if mso
                                        ]><style>
                                            .v-button {{
                                            background: transparent !important;
                                            }}
                                        </style><!
                                        [endif]-->
                                        <div class="v-text-align" align="left">
                                        <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://www.youtube.com/c/san99tiago" style="height:37px; v-text-anchor:middle; width:202px;" arcsize="11%"  stroke="f" fillcolor="#ec19ae"><w:anchorlock/><center style="color:#FFFFFF;"><![endif]-->
                                        <a
                                            href="https://www.youtube.com/c/san99tiago"
                                            target="_blank"
                                            class="v-button v-font-size"
                                            style="
                                            box-sizing: border-box;
                                            display: inline-block;
                                            text-decoration: none;
                                            -webkit-text-size-adjust: none;
                                            text-align: center;
                                            color: #ffffff;
                                            background-color: #ec19ae;
                                            border-radius: 4px;
                                            -webkit-border-radius: 4px;
                                            -moz-border-radius: 4px;
                                            width: 72%;
                                            max-width: 100%;
                                            overflow-wrap: break-word;
                                            word-break: break-word;
                                            word-wrap: break-word;
                                            mso-border-alt: none;
                                            font-size: 14px;
                                            "
                                        >
                                            <span
                                            class="v-line-height v-padding"
                                            style="
                                                display: block;
                                                padding: 10px 20px;
                                                line-height: 120%;
                                            "
                                            >YouTube</span
                                            >
                                        </a>
                                        <!--[if mso]></center></v:roundrect><![endif]-->
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                        </div>
                    </div>
                    </div>

                    <div
                    class="u-row-container"
                    style="padding: 0px; background-color: transparent"
                    >
                    <div
                        class="u-row"
                        style="
                        margin: 0 auto;
                        min-width: 320px;
                        max-width: 600px;
                        overflow-wrap: break-word;
                        word-wrap: break-word;
                        word-break: break-word;
                        background-color: transparent;
                        "
                    >
                        <div
                        style="
                            border-collapse: collapse;
                            display: table;
                            width: 100%;
                            height: 100%;
                            background-color: transparent;
                        "
                        >
                        <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->

                        <!--[if (mso)|(IE)]><td align="center" width="300" class="v-col-border" style="background-color: #ffffff;width: 300px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                        <div
                            class="u-col u-col-50"
                            style="
                            max-width: 320px;
                            min-width: 300px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div
                            style="
                                background-color: #ffffff;
                                height: 100%;
                                width: 100% !important;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                            "
                            >
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                                "
                            ><!--<![endif]-->
                                <table
                                id="u_content_image_3"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 0px 10px 60px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <table
                                        width="100%"
                                        cellpadding="0"
                                        cellspacing="0"
                                        border="0"
                                        >
                                        <tr>
                                            <td
                                            class="v-text-align"
                                            style="
                                                padding-right: 0px;
                                                padding-left: 0px;
                                            "
                                            align="center"
                                            >
                                            <a
                                                href="https://youtu.be/q9qkCpXLlGE"
                                                target="_blank"
                                            >
                                                <img
                                                align="center"
                                                border="0"
                                                src="{self.s3_url}/ses_images/image-8.png"
                                                alt="image"
                                                title="image"
                                                style="
                                                    outline: none;
                                                    text-decoration: none;
                                                    -ms-interpolation-mode: bicubic;
                                                    clear: both;
                                                    display: inline-block !important;
                                                    border: none;
                                                    height: auto;
                                                    float: none;
                                                    width: 100%;
                                                    max-width: 280px;
                                                "
                                                width="280"
                                                class="v-src-width v-src-max-width"
                                                />
                                            </a>
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]><td align="center" width="300" class="v-col-border" style="background-color: #ffffff;width: 300px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                        <div
                            class="u-col u-col-50"
                            style="
                            max-width: 320px;
                            min-width: 300px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div
                            style="
                                background-color: #ffffff;
                                height: 100%;
                                width: 100% !important;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                            "
                            >
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                                "
                            ><!--<![endif]-->
                                <table
                                id="u_content_heading_6"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 25px 10px 0px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <!--[if mso]><table width="100%"><tr><td><![endif]-->
                                        <h1
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            margin: 0px;
                                            line-height: 120%;
                                            text-align: left;
                                            word-wrap: break-word;
                                            font-size: 22px;
                                            font-weight: 400;
                                        "
                                        >
                                        <span
                                            ><span
                                            ><span
                                                ><span
                                                ><span
                                                    ><span
                                                    ><strong
                                                        >Last YouTube Video</strong
                                                    ></span
                                                    ></span
                                                ></span
                                                ></span
                                            ></span
                                            ></span
                                        >
                                        </h1>
                                        <!--[if mso]></td></tr></table><![endif]-->
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                id="u_content_text_6"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 5px 10px 10px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            font-size: 14px;
                                            line-height: 140%;
                                            text-align: left;
                                            word-wrap: break-word;
                                        "
                                        >
                                        <p style="line-height: 140%">
                                            Learn about AWS CDK by a hands-on tutorial
                                            deploying a Lambda Function from scratch.
                                        </p>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                id="u_content_text_13"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 5px 10px 10px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            font-size: 16px;
                                            line-height: 140%;
                                            text-align: left;
                                            word-wrap: break-word;
                                        "
                                        >
                                        <p style="line-height: 140%">
                                            <a
                                            rel="noopener"
                                            href="https://youtu.be/q9qkCpXLlGE"
                                            target="_blank"
                                            ><strong>Visit Us</strong></a
                                            >
                                        </p>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                        </div>
                    </div>
                    </div>

                    <div
                    class="u-row-container"
                    style="padding: 0px; background-color: transparent"
                    >
                    <div
                        class="u-row"
                        style="
                        margin: 0 auto;
                        min-width: 320px;
                        max-width: 600px;
                        overflow-wrap: break-word;
                        word-wrap: break-word;
                        word-break: break-word;
                        background-color: transparent;
                        "
                    >
                        <div
                        style="
                            border-collapse: collapse;
                            display: table;
                            width: 100%;
                            height: 100%;
                            background-color: transparent;
                        "
                        >
                        <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->

                        <!--[if (mso)|(IE)]><td align="center" width="150" class="v-col-border" style="background-color: #39cef6;width: 150px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                        <div
                            id="u_column_10"
                            class="u-col u-col-25"
                            style="
                            max-width: 320px;
                            min-width: 150px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div
                            style="
                                background-color: #39cef6;
                                height: 100%;
                                width: 100% !important;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                            "
                            >
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                                "
                            ><!--<![endif]-->
                                <table
                                id="u_content_image_4"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 46px 10px 10px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <table
                                        width="100%"
                                        cellpadding="0"
                                        cellspacing="0"
                                        border="0"
                                        >
                                        <tr>
                                            <td
                                            class="v-text-align"
                                            style="
                                                padding-right: 0px;
                                                padding-left: 0px;
                                            "
                                            align="center"
                                            >
                                            <img
                                                align="center"
                                                border="0"
                                                src="{self.s3_url}/ses_images/image-4.png"
                                                alt="image"
                                                title="image"
                                                style="
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                clear: both;
                                                display: inline-block !important;
                                                border: none;
                                                height: auto;
                                                float: none;
                                                width: 44%;
                                                max-width: 57.2px;
                                                "
                                                width="57.2"
                                                class="v-src-width v-src-max-width"
                                            />
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 0px 0px 30px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            font-size: 14px;
                                            color: #ffffff;
                                            line-height: 140%;
                                            text-align: center;
                                            word-wrap: break-word;
                                        "
                                        >
                                        <p style="line-height: 140%">
                                            <strong>Development</strong>
                                        </p>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]><td align="center" width="150" class="v-col-border" style="background-color: #39cef6;width: 150px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                        <div
                            id="u_column_11"
                            class="u-col u-col-25"
                            style="
                            max-width: 320px;
                            min-width: 150px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div
                            style="
                                background-color: #39cef6;
                                height: 100%;
                                width: 100% !important;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                            "
                            >
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                                "
                            ><!--<![endif]-->
                                <table
                                id="u_content_image_5"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 40px 10px 11px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <table
                                        width="100%"
                                        cellpadding="0"
                                        cellspacing="0"
                                        border="0"
                                        >
                                        <tr>
                                            <td
                                            class="v-text-align"
                                            style="
                                                padding-right: 0px;
                                                padding-left: 0px;
                                            "
                                            align="center"
                                            >
                                            <img
                                                align="center"
                                                border="0"
                                                src="{self.s3_url}/ses_images/image-9.png"
                                                alt="image"
                                                title="image"
                                                style="
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                clear: both;
                                                display: inline-block !important;
                                                border: none;
                                                height: auto;
                                                float: none;
                                                width: 30%;
                                                max-width: 39px;
                                                "
                                                width="39"
                                                class="v-src-width v-src-max-width"
                                            />
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 0px 0px 30px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            font-size: 14px;
                                            color: #ffffff;
                                            line-height: 140%;
                                            text-align: center;
                                            word-wrap: break-word;
                                        "
                                        >
                                        <p style="line-height: 140%">
                                            <strong>Learning</strong>
                                        </p>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]><td align="center" width="150" class="v-col-border" style="background-color: #39cef6;width: 150px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                        <div
                            id="u_column_12"
                            class="u-col u-col-25"
                            style="
                            max-width: 320px;
                            min-width: 150px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div
                            style="
                                background-color: #39cef6;
                                height: 100%;
                                width: 100% !important;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                            "
                            >
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                                "
                            ><!--<![endif]-->
                                <table
                                id="u_content_image_6"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 38px 10px 14px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <table
                                        width="100%"
                                        cellpadding="0"
                                        cellspacing="0"
                                        border="0"
                                        >
                                        <tr>
                                            <td
                                            class="v-text-align"
                                            style="
                                                padding-right: 0px;
                                                padding-left: 0px;
                                            "
                                            align="center"
                                            >
                                            <img
                                                align="center"
                                                border="0"
                                                src="{self.s3_url}/ses_images/image-5.png"
                                                alt="image"
                                                title="image"
                                                style="
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                clear: both;
                                                display: inline-block !important;
                                                border: none;
                                                height: auto;
                                                float: none;
                                                width: 32%;
                                                max-width: 41.6px;
                                                "
                                                width="41.6"
                                                class="v-src-width v-src-max-width"
                                            />
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 0px 0px 30px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            font-size: 14px;
                                            color: #ffffff;
                                            line-height: 140%;
                                            text-align: center;
                                            word-wrap: break-word;
                                        "
                                        >
                                        <p style="line-height: 140%">
                                            <strong>Tools</strong>
                                        </p>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]><td align="center" width="150" class="v-col-border" style="background-color: #39cef6;width: 150px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                        <div
                            class="u-col u-col-25"
                            style="
                            max-width: 320px;
                            min-width: 150px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div
                            style="
                                background-color: #39cef6;
                                height: 100%;
                                width: 100% !important;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                            "
                            >
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                                "
                            ><!--<![endif]-->
                                <table
                                id="u_content_image_7"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 33px 10px 11px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <table
                                        width="100%"
                                        cellpadding="0"
                                        cellspacing="0"
                                        border="0"
                                        >
                                        <tr>
                                            <td
                                            class="v-text-align"
                                            style="
                                                padding-right: 0px;
                                                padding-left: 0px;
                                            "
                                            align="center"
                                            >
                                            <img
                                                align="center"
                                                border="0"
                                                src="{self.s3_url}/ses_images/image-7.png"
                                                alt="image"
                                                title="image"
                                                style="
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                clear: both;
                                                display: inline-block !important;
                                                border: none;
                                                height: auto;
                                                float: none;
                                                width: 40%;
                                                max-width: 52px;
                                                "
                                                width="52"
                                                class="v-src-width v-src-max-width"
                                            />
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 0px 0px 30px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            font-size: 14px;
                                            color: #ffffff;
                                            line-height: 140%;
                                            text-align: center;
                                            word-wrap: break-word;
                                        "
                                        >
                                        <p style="line-height: 140%">
                                            <strong>AWS</strong>
                                        </p>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                        </div>
                    </div>
                    </div>

                    <div
                    class="u-row-container"
                    style="padding: 0px; background-color: transparent"
                    >
                    <div
                        class="u-row"
                        style="
                        margin: 0 auto;
                        min-width: 320px;
                        max-width: 600px;
                        overflow-wrap: break-word;
                        word-wrap: break-word;
                        word-break: break-word;
                        background-color: transparent;
                        "
                    >
                        <div
                        style="
                            border-collapse: collapse;
                            display: table;
                            width: 100%;
                            height: 100%;
                            background-color: transparent;
                        "
                        >
                        <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->

                        <!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-border" style="background-color: #ffffff;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                        <div
                            class="u-col u-col-100"
                            style="
                            max-width: 320px;
                            min-width: 600px;
                            display: table-cell;
                            vertical-align: top;
                            "
                        >
                            <div
                            style="
                                background-color: #ffffff;
                                height: 100%;
                                width: 100% !important;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                            "
                            >
                            <!--[if (!mso)&(!IE)]><!--><div
                                class="v-col-border"
                                style="
                                box-sizing: border-box;
                                height: 100%;
                                padding: 0px;
                                border-top: 0px solid transparent;
                                border-left: 0px solid transparent;
                                border-right: 0px solid transparent;
                                border-bottom: 0px solid transparent;
                                border-radius: 0px;
                                -webkit-border-radius: 0px;
                                -moz-border-radius: 0px;
                                "
                            ><!--<![endif]-->
                                <table
                                id="u_content_text_15"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 40px 80px 10px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            font-size: 14px;
                                            line-height: 160%;
                                            text-align: center;
                                            word-wrap: break-word;
                                        "
                                        >
                                        <p style="font-size: 14px; line-height: 160%">
                                            if you have any questions, please email us
                                            at
                                            <a
                                            rel="noopener"
                                            href="mailto:san99tiago@gmail.com?subject=FAQ%20to%20san99tiago"
                                            target="_blank"
                                            >san99tiago@gmail.com</a
                                            >
                                            or visit our FAQS. Thanks for checking out
                                            our website.
                                        </p>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 20px 0px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <table
                                        height="0px"
                                        align="center"
                                        border="0"
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                            border-collapse: collapse;
                                            table-layout: fixed;
                                            border-spacing: 0;
                                            mso-table-lspace: 0pt;
                                            mso-table-rspace: 0pt;
                                            vertical-align: top;
                                            border-top: 1px solid #bbbbbb;
                                            -ms-text-size-adjust: 100%;
                                            -webkit-text-size-adjust: 100%;
                                        "
                                        >
                                        <tbody>
                                            <tr style="vertical-align: top">
                                            <td
                                                style="
                                                word-break: break-word;
                                                border-collapse: collapse !important;
                                                vertical-align: top;
                                                font-size: 0px;
                                                line-height: 0px;
                                                mso-line-height-rule: exactly;
                                                -ms-text-size-adjust: 100%;
                                                -webkit-text-size-adjust: 100%;
                                                "
                                            >
                                                <span>&#160;</span>
                                            </td>
                                            </tr>
                                        </tbody>
                                        </table>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 10px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div align="center">
                                        <div style="display: table; max-width: 187px">
                                            <!--[if (mso)|(IE)]><table width="187" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-collapse:collapse;" align="center"><table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse; mso-table-lspace: 0pt;mso-table-rspace: 0pt; width:187px;"><tr><![endif]-->

                                            <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 15px;" valign="top"><![endif]-->
                                            <table
                                            align="left"
                                            border="0"
                                            cellspacing="0"
                                            cellpadding="0"
                                            width="32"
                                            height="32"
                                            style="
                                                width: 32px !important;
                                                height: 32px !important;
                                                display: inline-block;
                                                border-collapse: collapse;
                                                table-layout: fixed;
                                                border-spacing: 0;
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                                vertical-align: top;
                                                margin-right: 15px;
                                            "
                                            >
                                            <tbody>
                                                <tr style="vertical-align: top">
                                                <td
                                                    align="left"
                                                    valign="middle"
                                                    style="
                                                    word-break: break-word;
                                                    border-collapse: collapse !important;
                                                    vertical-align: top;
                                                    "
                                                >
                                                    <a
                                                    href="https://www.linkedin.com/in/san99tiago/"
                                                    title="LinkedIn"
                                                    target="_blank"
                                                    >
                                                    <img
                                                        src="{self.s3_url}/ses_images/image-1.png"
                                                        alt="LinkedIn"
                                                        title="LinkedIn"
                                                        width="32"
                                                        style="
                                                        outline: none;
                                                        text-decoration: none;
                                                        -ms-interpolation-mode: bicubic;
                                                        clear: both;
                                                        display: block !important;
                                                        border: none;
                                                        height: auto;
                                                        float: none;
                                                        max-width: 32px !important;
                                                        "
                                                    />
                                                    </a>
                                                </td>
                                                </tr>
                                            </tbody>
                                            </table>
                                            <!--[if (mso)|(IE)]></td><![endif]-->

                                            <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 15px;" valign="top"><![endif]-->
                                            <table
                                            align="left"
                                            border="0"
                                            cellspacing="0"
                                            cellpadding="0"
                                            width="32"
                                            height="32"
                                            style="
                                                width: 32px !important;
                                                height: 32px !important;
                                                display: inline-block;
                                                border-collapse: collapse;
                                                table-layout: fixed;
                                                border-spacing: 0;
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                                vertical-align: top;
                                                margin-right: 15px;
                                            "
                                            >
                                            <tbody>
                                                <tr style="vertical-align: top">
                                                <td
                                                    align="left"
                                                    valign="middle"
                                                    style="
                                                    word-break: break-word;
                                                    border-collapse: collapse !important;
                                                    vertical-align: top;
                                                    "
                                                >
                                                    <a
                                                    href="https://www.instagram.com/san99tiago/"
                                                    title="Instagram"
                                                    target="_blank"
                                                    >
                                                    <img
                                                        src="{self.s3_url}/ses_images/image-2.png"
                                                        alt="Instagram"
                                                        title="Instagram"
                                                        width="32"
                                                        style="
                                                        outline: none;
                                                        text-decoration: none;
                                                        -ms-interpolation-mode: bicubic;
                                                        clear: both;
                                                        display: block !important;
                                                        border: none;
                                                        height: auto;
                                                        float: none;
                                                        max-width: 32px !important;
                                                        "
                                                    />
                                                    </a>
                                                </td>
                                                </tr>
                                            </tbody>
                                            </table>
                                            <!--[if (mso)|(IE)]></td><![endif]-->

                                            <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 15px;" valign="top"><![endif]-->
                                            <table
                                            align="left"
                                            border="0"
                                            cellspacing="0"
                                            cellpadding="0"
                                            width="32"
                                            height="32"
                                            style="
                                                width: 32px !important;
                                                height: 32px !important;
                                                display: inline-block;
                                                border-collapse: collapse;
                                                table-layout: fixed;
                                                border-spacing: 0;
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                                vertical-align: top;
                                                margin-right: 15px;
                                            "
                                            >
                                            <tbody>
                                                <tr style="vertical-align: top">
                                                <td
                                                    align="left"
                                                    valign="middle"
                                                    style="
                                                    word-break: break-word;
                                                    border-collapse: collapse !important;
                                                    vertical-align: top;
                                                    "
                                                >
                                                    <a
                                                    href="https://www.youtube.com/c/san99tiago"
                                                    title="YouTube"
                                                    target="_blank"
                                                    >
                                                    <img
                                                        src="{self.s3_url}/ses_images/image-3.png"
                                                        alt="YouTube"
                                                        title="YouTube"
                                                        width="32"
                                                        style="
                                                        outline: none;
                                                        text-decoration: none;
                                                        -ms-interpolation-mode: bicubic;
                                                        clear: both;
                                                        display: block !important;
                                                        border: none;
                                                        height: auto;
                                                        float: none;
                                                        max-width: 32px !important;
                                                        "
                                                    />
                                                    </a>
                                                </td>
                                                </tr>
                                            </tbody>
                                            </table>
                                            <!--[if (mso)|(IE)]></td><![endif]-->

                                            <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 0px;" valign="top"><![endif]-->
                                            <table
                                            align="left"
                                            border="0"
                                            cellspacing="0"
                                            cellpadding="0"
                                            width="32"
                                            height="32"
                                            style="
                                                width: 32px !important;
                                                height: 32px !important;
                                                display: inline-block;
                                                border-collapse: collapse;
                                                table-layout: fixed;
                                                border-spacing: 0;
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                                vertical-align: top;
                                                margin-right: 0px;
                                            "
                                            >
                                            <tbody>
                                                <tr style="vertical-align: top">
                                                <td
                                                    align="left"
                                                    valign="middle"
                                                    style="
                                                    word-break: break-word;
                                                    border-collapse: collapse !important;
                                                    vertical-align: top;
                                                    "
                                                >
                                                    <a
                                                    href="https://github.com/san99tiago"
                                                    title="GitHub"
                                                    target="_blank"
                                                    >
                                                    <img
                                                        src="{self.s3_url}/ses_images/image-6.png"
                                                        alt="GitHub"
                                                        title="GitHub"
                                                        width="32"
                                                        style="
                                                        outline: none;
                                                        text-decoration: none;
                                                        -ms-interpolation-mode: bicubic;
                                                        clear: both;
                                                        display: block !important;
                                                        border: none;
                                                        height: auto;
                                                        float: none;
                                                        max-width: 32px !important;
                                                        "
                                                    />
                                                    </a>
                                                </td>
                                                </tr>
                                            </tbody>
                                            </table>
                                            <!--[if (mso)|(IE)]></td><![endif]-->

                                            <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                                        </div>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                id="u_content_menu_2"
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 10px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div class="menu" style="text-align: center">
                                        <!--[if (mso)|(IE)]><table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center"><tr><![endif]-->

                                        <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->

                                        <a
                                            href="https://san99tiago.com"
                                            target="_self"
                                            style="
                                            padding: 5px 15px;
                                            display: inline-block;
                                            color: #000000;
                                            font-size: 14px;
                                            text-decoration: none;
                                            "
                                            class="v-padding v-font-size"
                                        >
                                            Home
                                        </a>

                                        <!--[if (mso)|(IE)]></td><![endif]-->

                                        <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->
                                        <span
                                            style="
                                            padding: 5px 15px;
                                            display: inline-block;
                                            color: #000000;
                                            font-size: 14px;
                                            "
                                            class="v-padding v-font-size hide-mobile"
                                        >
                                            |
                                        </span>
                                        <!--[if (mso)|(IE)]></td><![endif]-->

                                        <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->

                                        <a
                                            href="https://san99tiago.com/experience"
                                            target="_self"
                                            style="
                                            padding: 5px 15px;
                                            display: inline-block;
                                            color: #000000;
                                            font-size: 14px;
                                            text-decoration: none;
                                            "
                                            class="v-padding v-font-size"
                                        >
                                            Experience
                                        </a>

                                        <!--[if (mso)|(IE)]></td><![endif]-->

                                        <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->
                                        <span
                                            style="
                                            padding: 5px 15px;
                                            display: inline-block;
                                            color: #000000;
                                            font-size: 14px;
                                            "
                                            class="v-padding v-font-size hide-mobile"
                                        >
                                            |
                                        </span>
                                        <!--[if (mso)|(IE)]></td><![endif]-->

                                        <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->

                                        <a
                                            href="https://san99tiago.com/contact"
                                            target="_self"
                                            style="
                                            padding: 5px 15px;
                                            display: inline-block;
                                            color: #000000;
                                            font-size: 14px;
                                            text-decoration: none;
                                            "
                                            class="v-padding v-font-size"
                                        >
                                            Contact
                                        </a>

                                        <!--[if (mso)|(IE)]></td><![endif]-->

                                        <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->
                                        <span
                                            style="
                                            padding: 5px 15px;
                                            display: inline-block;
                                            color: #000000;
                                            font-size: 14px;
                                            "
                                            class="v-padding v-font-size hide-mobile"
                                        >
                                            |
                                        </span>
                                        <!--[if (mso)|(IE)]></td><![endif]-->

                                        <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->

                                        <a
                                            href="https://san99tiago.com/pdfs/cv-santiago-garcia-arango.pdf"
                                            target="_self"
                                            style="
                                            padding: 5px 15px;
                                            display: inline-block;
                                            color: #000000;
                                            font-size: 14px;
                                            text-decoration: none;
                                            "
                                            class="v-padding v-font-size"
                                        >
                                            CV
                                        </a>

                                        <!--[if (mso)|(IE)]></td><![endif]-->

                                        <!--[if (mso)|(IE)]></tr></table><![endif]-->
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <table
                                style="font-family: arial, helvetica, sans-serif"
                                role="presentation"
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                border="0"
                                >
                                <tbody>
                                    <tr>
                                    <td
                                        class="v-container-padding-padding"
                                        style="
                                        overflow-wrap: break-word;
                                        word-break: break-word;
                                        padding: 10px 10px 40px;
                                        font-family: arial, helvetica, sans-serif;
                                        "
                                        align="left"
                                    >
                                        <div
                                        class="v-text-align v-line-height v-font-size"
                                        style="
                                            font-size: 14px;
                                            line-height: 160%;
                                            text-align: center;
                                            word-wrap: break-word;
                                        "
                                        >
                                        <p style="font-size: 14px; line-height: 160%">
                                            you have received this email as a registered
                                            user of
                                            <a
                                            rel="noopener"
                                            href="https://san99tiago.com"
                                            target="_blank"
                                            >san99tiago.com</a
                                            >
                                        </p>
                                        <p style="font-size: 14px; line-height: 160%">
                                            please reply with subject "UNSUBSCRIBE" to
                                            end the subcription.
                                        </p>
                                        <p style="font-size: 14px; line-height: 160%">
                                             
                                        </p>
                                        <p style="font-size: 14px; line-height: 160%">
                                            Medellín, Colombia. san99tiago All rights
                                            reserved.
                                        </p>
                                        </div>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>

                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                        </div>
                    </div>
                    </div>

                    <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
                </td>
                </tr>
            </tbody>
            </table>
            <!--[if mso]></div><![endif]-->
            <!--[if IE]></div><![endif]-->
        </body>
        </html>
        """
