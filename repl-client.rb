require "io/wait"
require "socket"

$input = ""
$input.force_encoding("UTF-8")

def repl_send code, strip_none=false
  sock = TCPSocket.new "localhost", 1951
  sock.send code.strip, 0
  sock.wait
  out = sock.recv(sock.nread).strip
  puts strip_none ? out.gsub(/\s*None$/, "\n") : out
  $stdout.flush
  sock.close
end

def balanced? code
  s = code.clone
  s.gsub! /;;.*/, ""
  s.gsub! /\\./, ""
  s.gsub! /"[^"]*"/, "\"\""
  s.gsub! /[^\(\)\[\]\{\}"]/, ""
  until s.gsub!(/\(\)|\[\]|\{\}|""/, "").nil?; end
  s.empty?
end

repl_send DATA.read.strip, true

while true
  print "\n>>> "
  $input += $stdin.gets.force_encoding("UTF-8")
  if balanced? $input
    repl_send $input
    $input = ""
  end
end

__END__
(do
  (import hy)
  (import platform)
  (import bpy.app)
  (print "; Blender Hy REPL")
  (print (.format "; {appname} {version}"
                  :appname hy.__appname__ 
                  :version hy.__version__))
  (print (.format "; {py}({build}) {pyversion} on {os}"
                  :py (platform.python-implementation)
                  :build (. (platform.python-build) [0])
                  :pyversion (platform.python-version)
                  :os (platform.system)))
  (print (.format "; Blender {version} {date} {time} {hash}"
                  :version bpy.app.version-string
                  :date (.decode bpy.app.build-date "utf-8")
                  :time (.decode bpy.app.build-time "utf-8")
                  :hash (.decode bpy.app.build-hash "utf-8"))))