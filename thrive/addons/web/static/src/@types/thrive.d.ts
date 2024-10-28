interface ThriveModule {
    deps: string[];
    fn: ThriveModuleFactory;
    ignoreMissingDeps: boolean;
}

type ThriveModuleFactory<T = string> = (require: (dependency: T) => any) => any;

type ThriveModuleDefineFn = <T = string>(name: string, deps: T[], factory: ThriveModuleFactory<T>, lazy?: boolean) => void;

class ModuleLoader {
    define: ThriveModuleDefineFn;
    factories: Map<string, ThriveModule>;
    failed: Set<string>;
    jobs: Set<string>;
    modules: Map<string, any>;
}

declare const thrive: {
    csrf_token: string;
    debug: string;
    define: ThriveModuleDefineFn;
    loader: ModuleLoader;
};
