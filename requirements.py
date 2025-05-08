import os
import re
import pkg_resources

def find_imports_in_file(file_path):
  with open(file_path, 'r') as file:
    content = file.read()
  imports = re.findall(r'^\s*(?:import|from)\s+([a-zA-Z0-9_\.]+)', content, re.MULTILINE)
  return imports

def get_installed_packages():
  installed_packages = {pkg.key for pkg in pkg_resources.working_set}
  return installed_packages

def generate_requirements(directory):
  installed_packages = get_installed_packages()
  all_imports = set()

  for root, _, files in os.walk(directory):
    for file in files:
      if file.endswith('.py'):
        file_path = os.path.join(root, file)
        imports = find_imports_in_file(file_path)
        all_imports.update(imports)

  requirements = set()
  for imp in all_imports:
    package = imp.split('.')[0]
    if package in installed_packages:
      requirements.add(package)

  return requirements

if __name__ == "__main__":
  project_directory = "/home/tigo/Desktop/SwellProject/SWELL_TRADING_BOT"
  requirements = generate_requirements(project_directory)

  with open(os.path.join(project_directory, 'requirements.txt'), 'w') as req_file:
    req_file.write('\n'.join(sorted(requirements)))

  print("requirements.txt has been generated.")