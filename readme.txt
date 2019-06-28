<p>This is a work in progress project mainly focused on Network configuration management and automation. Project is being developed with <strong>Django</strong> and <strong>Python</strong> on the backend, and <strong>HTML</strong>, <strong>CSS</strong> and <strong>JavaScript</strong> on the front-end.</p>
<p>I will create a proper documentation that includes the functionalities already available, meanwhile, below are a brief description of some of the functionalities available:<p>
<ol>
<li>Create Branches.</li>
<li>Register Network devices and associate them to a branch.</li>
<li>Support for model driven APIs such RESTCONF, and legacy API such SSH using NetMiko.</li>
<li>On routers only retrieving configuration and interfaces are available on Cisco Devices only at this moment.</li>
<li>On Switches, only retrieving configuration, interfaces, changing port VLAN assignment, Synchronizing VLANs are available using RESTCONF on Cisco Devices only at this moment.</li>
</ol>

<p>For portability sake, I decided to use <strong>SQLITE</strong> as the database engine for this project, this is subject to modification in the future if I am in the need of a more scalable <strong>DBMS</strong> such <strong>PostgreSQL</strong> or <strong>MySQL</strong>.</p>

<p><strong>Note:</strong> credentials used to interact with devices is separate from Django built-in User Authentication system. Devices credentials are defined during creation of devices and store in the database as clear text which could present security risks depending on how and where you use this.<p>

<p>If you have any questions, feel free to contact at the emails below or at my <strong>LinkedIn</strong> profile <strong>Francisco Sencion</strong>:</p>
<ul>
<li>francisco.sencion@gmail.com</li>
<li>francisco.sencion@yahoo.com</li>
</ul>
