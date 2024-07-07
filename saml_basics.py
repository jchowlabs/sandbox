import datetime
import xml.etree.ElementTree as ET

def generate_saml_assertion(issuer, subject, audience):
    # Define namespaces
    ns = {
        'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
        'ds': 'http://www.w3.org/2000/09/xmldsig#',
    }

    # Create root element for the assertion
    assertion = ET.Element('saml:Assertion', ns)
    assertion.set('Version', '2.0')
    assertion.set('IssueInstant', datetime.datetime.utcnow().isoformat() + 'Z')
    assertion.set('ID', '_'.join(['ID', str(datetime.datetime.now().timestamp())]))

    # Create issuer element
    issuer_element = ET.SubElement(assertion, 'saml:Issuer', ns)
    issuer_element.text = issuer

    # Create subject element
    subject_element = ET.SubElement(assertion, 'saml:Subject', ns)
    name_id = ET.SubElement(subject_element, 'saml:NameID', ns)
    name_id.text = subject

    # Create conditions element
    conditions = ET.SubElement(assertion, 'saml:Conditions', ns)
    conditions.set('NotBefore', datetime.datetime.utcnow().isoformat() + 'Z')
    conditions.set('NotOnOrAfter', (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat() + 'Z')

    # Create audience restriction element
    audience_restriction = ET.SubElement(conditions, 'saml:AudienceRestriction', ns)
    audience_element = ET.SubElement(audience_restriction, 'saml:Audience', ns)
    audience_element.text = audience

    # Convert assertion to XML string
    assertion_xml = ET.tostring(assertion)

    return assertion_xml

def authenticate():
    username = input("Enter username: ")
    password = input("Enter password: ")  

    if username == "jchow" and password == "Hello123!!":
        return True
    else:
        return False

if __name__ == "__main__":

    if authenticate():
        issuer = "https://jchowlabs.com"
        subject = "jchow@jchowlabs.com"
        audience = "https://service.jchowlabs.com"

        assertion_xml = generate_saml_assertion(issuer, subject, audience)

        print()
        print("SAML Assertion:")
        print(assertion_xml.decode('utf-8')) 

    else:
        print("Invalid username or password. Authentication failed.")
