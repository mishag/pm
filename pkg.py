# Package: (Name, Version, Deps)


# List packages
# Add package
# Install package

from collections import defaultdict


class Constraint:
    EQ = 0
    GT = 1
    GE = 2


class Dependency:
    CONSTRAINT_EQ = 0
    CONSTRAINT_GT = 1
    CONSTRAINT_GE = 2

    _constraint_symbols = {
        CONSTRAINT_EQ: '==',
        CONSTRAINT_GE: '>=',
        CONSTRAINT_GT: '>'
    }

    def __init__(self, name, version, constraint):
        self._name = name
        self._version = version
        self._constraint = constraint

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def constraint(self):
        return self._constraint

    def validate(self, package):
        if package.name != self.name:
            return False

        if self.constraint == Dependency.CONSTRAINT_EQ:
            return self.version == package.version

        if self.constraint == Dependency.CONSTRAINT_GT:
            return package.version > self.version

        if self.constraint == Dependency.CONSTRAINT_GE:
            return package.version >= self.version

    def __str__(self):
        return "{} {}{}".format(
            self.name,
            Dependency._constraint_symbols[self.constraint],
            self.version)

    def __repr__(self):
        return str(self)


class Package:

    def __init__(self, name, version, deps):
        self._name = name
        self._version = version
        self._deps = deps

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def dependencies(self):
        return self._deps

    def __eq__(self, other):
        return self._name == other._name and self._version == other._version

    def __hash__(self):
        return hash((self._name, self._version))

    def __str__(self):
        return "{}-{}".format(self._name, self._version)

    def __repr__(self):
        return "<{}-{}>".format(self._name, self._version)


class PackageRepository:
    def __init__(self):
        self._packages = defaultdict(set)

    def find_packages(self,
                      name,
                      version,
                      constraint=Dependency.CONSTRAINT_EQ):
        package_set = self._packages.get(name, None)
        if package_set is None:
            return None

        results = []

        for p in package_set:
            dep = Dependency(name, version, constraint)
            if dep.validate(p):
                results.append(p)

        return results

    def list_packages(self, package_name=None):
        if package_name is not None:
            return self._packages.get(package_name, [])

        results = []
        for package_set in self._packages.values():
            results.extend(list(package_set))

        return results

    def add_package(self, package):
        if not isinstance(package, Package):
            raise RuntimeError("Expecting object of type Package")

        for dep in package.dependencies:
            if not self.find_packages(dep.name,
                                      dep.version,
                                      constraint=dep.constraint):
                raise RuntimeError(
                    "Cannot add package: {}. "
                    "Required dependency: {} is not found"
                    .format(package, dep))

        existing_packages = self._packages[package.name]
        if package in existing_packages:
            raise RuntimeError("Package {} already exists".format(package))

        existing_packages.add(package)


class PackageDb:
    def __init__(self):
        self._installed_packages = defaultdict(set)

    def install_package(self,
                        name,
                        version,
                        constraint=Dependency.CONSTRAINT_GE):
        pass
