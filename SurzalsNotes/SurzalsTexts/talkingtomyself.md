# Surzals Notes

Here be the notes I take while ethical hacking and malware analysis/malware development. I will be adding to this as I go, and I will be adding more sections as I go. This is not a complete list of all the things I have learned, but it is a good starting point for anyone who wants to learn about ethical hacking and malware analysis/development.

## Talking to myself

So we need to talk web vulnerabilities, I've not actually dived in. So lets begin

## Translating Ipv6 to Ipv4

So apparently there is only a very small subset of addresses actually mappable to ipv4, and the rest are not. So if you have an ipv6 address, you can check if it is mappable to ipv4 by checking if it starts with ::ffff: followed by the ipv4 address in hexadecimal. For example, the ipv6 address ::ffff:192.0.2.128 is mappable to the ipv4 address 192.0.2.128. However, you can still ftp/ssh/do all that stuff, simply use the ipv6 address instead of the ipv4 address. For example, to ssh to the ipv6 address ::ffff:192.0.2.128, you would use the command `ssh user@::ffff:192.0.2.128`. In addition, despite it being protocols, you can still https:// to an ipv6 address, simply use the ipv6 address in the URL. For example, to https:// to the ipv6 address ::ffff:192.0.2.128  you would use the URL `https://[::ffff:192.0.2.128]`. ALWAYS REMEMBER THE BRACKETS.

### Pinging IPV6 addresses

To ping an ipv6 address, you can use the command `ping6` followed by the ipv6 address. For example, to ping the ipv6 address ::ffff:192.0.2.128, you would use the command `ping6 ::ffff:192.0.2.128`. Remember the first two hexacts of the ipv6 address are always 0, so you can omit them when pinging. For example, you can also ping the ipv6 address ::ffff:192.0.2.128 by using the command `ping6 ::ffff:192.0.2.128`.

### Using IPV6 addresses in URLs

To use an ipv6 address in a URL, you need to enclose the ipv6 address in square brackets. For example, to access the website at the ipv6 address ::ffff:192.0.2.128, you would use the URL `https://[::ffff:192.0.2.128]`.

### Per Interface IPV6 addresses

Each network interface on a device can have its own ipv6 address. To find the ipv6 address of a specific network interface, you can use the command `ip -6 addr show <interface>`, where `<interface>` is the name of the network interface. For example, to find the ipv6 address of the eth0 interface, you would use the command `ip -6 addr show eth0`. This will display the ipv6 address assigned to the eth0 interface.
This is extremely helpful in situations where you have multiple network interfaces and you want to know which ipv6 address is associated with which interface. It can also be helpful when you are trying to connect to a specific service that is only available on a certain interface.

### Types of IPV6 addresses

There are several types of ipv6 addresses, including:
1.) Unicast addresses: These are used to identify a single interface on a device. They are typically used for communication between devices on the same network.

2.) Multicast addresses: These are used to identify a group of interfaces on a device. They are typically used for communication between devices on different networks.

3.) Anycast addresses: These are used to identify a group of interfaces on a device, but they are typically used for communication between devices on the same network.

4.) Link-local addresses: These are used to identify interfaces on a device that are only valid within the local network. They are typically used for communication between devices on the same network.

5.) Global unicast addresses: These are used to identify interfaces on a device that are valid globally. They are typically used for communication between devices on different networks.

## Pivot Types

1.) Network Pivoting: This involves things like SSH tunneling, VPNs, and proxying. This allows an attacker to use the compromised system as a gateway to access other systems on the same network. Meterpreter's autoroute and chisel/ligolo-ng are good examples of tools that can be used for network pivoting. The classic act of borrowing into the victim's network cable.

2.) Identity Pivoting: This involves using things like stolen Kerebos tickets, stolen session cookies, or stolen credentials to access other systems on the same network. This can be done by using the compromised system to scan for other vulnerable systems, or by using it to launch attacks against other systems on the network. Other examples include OAuth token theft, SAML token theft, and JWT token theft. Think moving through trust relationships, only the subnets themselves.

3.) Application Pivoting: This involves using things like Web app -> database, microservice -> database, or web app -> microservice vulnerabilities to access other systems on the same network. Other routers include SaaS to third party APIs, Container to cloud metadata service, and web app to internal services. You're basically riding the app's backend trust graph.

4.) Gateway Pivoting: This involves compromising the routing or boundary device and using it as a vantage point. Simple and clean :D. Like a hypervisor pivot, or a router pivot, or a firewall pivot. The model is simply controlling the network wiring from the inside.

5.) Protocol Pivoting:  This involves pivoting off things like SMB, RDP, LDAP, and DNS among other protocols. Mental mode is simple, if the network blocks X, speak Y.

6.) Host Pivoting: This is stuff like mounted share folders, stored credentials, and scheduled tasks or services. Mental mode: What this host trusts becomes your path to exploitation.

7.) Cloud Pivoting: So alot of this is pretty simple AWS IAM -> Lambda -> EC2 kinda deal, or perhaps Azure AD -> Graph API -> Key Vault is more your style? Its lateral movement but with your packets.

8.) Supply Chain Pivoting: This is just following how the systems integrate together. So CI/CD -> cloud. Maybe even Github -> secrets -> production if you like looking at source code all day. You're following the automation routes to the core.

9.) Social Engineering Pivoting: Using compromised human accounts or communication channels to reach new systems. One compromised email and a password reset == PROFIT. You're moving through human trust now, not technical.

## Web Cache Vulnerabilities

Cache Rules: These determine what can be cached, and for how long. Cache rules are set by the website owner, and they can be used to prevent sensitive content from being cached. However, if the cache rules are not set correctly, it can lead to vulnerabilities such as web cache deception and web cache poisoning.

Cache Keys: These are the values that the cache uses to identify and store content. If the cache keys are not properly configured, it can lead to vulnerabilities such as web cache poisoning, where an attacker can manipulate the cache to serve malicious content to users.

### Web Cache Deception

Web cache deception is a vulnerability that enables an attacker to trick a web cache into storing sensitive, dynamic content. It's caused by discrepancies between how the cache server and origin server handle requests.

In a web cache deception attack, an attacker persuades a victim to visit a malicious URL, inducing the victim's browser to make an ambiguous request for sensitive content. The cache misinterprets this as a request for a static resource and stores the response. The attacker can then request the same URL to access the cached response, gaining unauthorized access to private information.

### Example of Web Cache Deception

Identify a target endpoint that returns a dynamic response containing sensitive info. Craft a URL that appends a static file extension (e.g., .jpg) to the endpoint, making it appear as a request for a static resource. Focus on endpoints that support GET, HEAD, or POST methods, as these are more likely to be cached. Persuade a victim to visit the crafted URL, causing the cache to store the sensitive response. Finally, request the same URL to access the cached response and retrieve the sensitive information.

### Using a cache buster

While testing for discrepancies and crafting a web cache deception exploit, make sure that each request you send has a different cache key. Otherwise, you may be served cached responses, which will impact your test results.

As both URL path and any query parameters are typically included in the cache key, you can change the key by adding a query string to the path and changing it each time you send a request. Automate this process using the Param Miner extension. To do this, once you've installed the extension, click on the top-level Param miner > Settings menu, then select Add dynamic cachebuster. Burp now adds a unique query string to every request that you make. You can view the added query strings in the Logger tab.

Watch out for this when testing for web cache vulnerabilities, as it can lead to false negatives if you are served cached responses instead of the actual responses from the server.

### Static Extension Cache Rules

Some web caches are configured to only cache responses for requests that have a static file extension, such as .jpg, .css, or .js. This means that if you want to test for web cache vulnerabilities on a website that uses this type of cache configuration, you will need to craft your requests in a way that includes a static file extension in the URL. For example, if you are testing for web cache deception on a dynamic endpoint like /profile, you could craft a request to /profile.jpg to see if the response is cached.

### Cached-Response Detection

When testing for web cache vulnerabilities, it's important to be able to detect when you are being served a cached response. This can be done by looking for certain HTTP headers that indicate that the response is coming from the cache, such as "X-Cache" or "X-Cache-Hit". Additionally, you can also look for differences in the response time, as cached responses are typically faster than non-cached responses.

### Exploiting delimiter discrepancies

You may be able to use a delimiter discrepancy to add a static extension to the path that is viewed by the cache, but not the origin server. To do this, you'll need to identify a character that is used as a delimiter by the origin server but not the cache.

Firstly, find characters that are used as delimiters by the origin server. Start this process by adding an arbitrary string to the URL of your target endpoint. For example, modify /settings/users/list to /settings/users/listaaa. You'll use this response as a reference when you start testing delimiter characters. Next, test various characters as delimiters by inserting them between the original path and the arbitrary string. For example, you could test /settings/users/list/aaa, /settings/users/list?aaa, or /settings/users/list#aaa. After each request, compare the response to your reference response to determine if the delimiter character is being treated differently by the cache and the origin server. If you find a character that is treated as a delimiter by the origin server but not by the cache, you can use it to craft a URL that includes a static extension for the cache while still being processed as a dynamic request by the origin server.

### Exploiting normalization by the origin server

Some web caches do not normalize URLs before caching responses, while the origin server does. This can lead to vulnerabilities if the cache treats different URLs as the same resource, while the origin server treats them as different resources. For example, if the cache does not normalize URLs, it may treat /profile and /profile/ as the same resource and cache the response for both URLs. However, if the origin server normalizes URLs, it may treat /profile and /profile/ as different resources and return different responses for each URL. An attacker can exploit this discrepancy by crafting a URL that is treated as a static resource by the cache but is processed as a dynamic request by the origin server, allowing them to access sensitive information or perform unauthorized actions.

#### HOW TO PREVENT

1.) Always use Cache-Control headers to mark dynamic resources, set with the directives no-store and private.
2.) Configure your CDN settings so that your caching rules don't override the Cache-Control header.
3.) Activate any protection that your CDN has against web cache deception attacks. Many CDNs enable you to set a cache rule that verifies that the response Content-Type matches the request's URL file extension. For example, Cloudflare's Cache Deception Armor.
4.) Verify that there aren't any discrepancies between how the origin server and the cache interpret URL paths.

### Web Cache Poisoning

Web cache poisoning is a vulnerability that allows an attacker to manipulate the content stored in a web cache, causing it to serve malicious or incorrect content to users. This can lead to various attacks, including the distribution of malware, phishing, or the exposure of sensitive information.

In a web cache poisoning attack, an attacker crafts a malicious request that is stored in the cache. When other users access the same URL, they receive the poisoned content instead of the legitimate content. This can be particularly dangerous if the poisoned content contains malware or misleading information.

#### Example of Web Cache Poisoning

### Server-Side Request Forgery (SSRF)

### XXE Injection

### NoSQL Injection

### API Testing

### Information Disclosure

### Access Control Issues

### File Upload Vulnerabilities

### Race Conditions

### Business Logic Flaws

### Command Injection

### Path Traversal

### Authentication Bypass

### SQL Injection

### DOM-Based client-side XPath Injection

DOM-based XPath-injection vulnerabilities arise when a script incorporates attacker-controllable data into an XPath query. An attacker may be able to use this behavior to construct a URL that, if visited by another application user, will trigger the execution of an arbitrary XPath query, which could cause different data to be retrieved and processed by the website.

## HTTP Options per Method

1.) GET: This method is used to retrieve data from a server. It is typically used for fetching web pages, images, and other resources. GET requests can be cached and remain in the browser history.

2.) POST: This method is used to send data to a server, often for creating or updating resources. POST requests are not cached and do not remain in the browser history.

3.) PUT: This method is used to update an existing resource or create a new resource if it does not exist. Like POST, PUT requests are not cached and do not remain in the browser history.

4.) DELETE: This method is used to delete a resource on the server. DELETE requests are not cached and do not remain in the browser history.

5.) HEAD: This method is similar to GET, but it only retrieves the headers of a resource, not the body. It is often used for checking if a resource has been modified or for retrieving metadata.

6.) OPTIONS: This method is used to describe the communication options for the target resource. It can be used to determine which HTTP methods are supported by the server for a specific resource.

7.) PATCH: This method is used to apply partial modifications to a resource. It is typically used for updating specific fields of a resource without replacing the entire resource.

## to be continued

Stuff I need to add.
