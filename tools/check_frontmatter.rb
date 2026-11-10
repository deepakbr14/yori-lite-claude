require 'yaml'
root=File.expand_path('..',__dir__)
names=[]
Dir[File.join(root,'skills/*/SKILL.md')].each do |path|
  text=File.read(path)
  data=YAML.safe_load(text.split('---',3)[1])
  raise 'Invalid YAML skill' unless data.is_a?(Hash) && data['name']==File.basename(File.dirname(path)) && data['description'].is_a?(String) && !data['description'].empty?
  names << data['name']
end
raise 'Missing or duplicate skills' unless names.length==5 && names.uniq.length==5
puts 'PASS: five skill YAML frontmatters parsed with unique matching names and descriptions.'
