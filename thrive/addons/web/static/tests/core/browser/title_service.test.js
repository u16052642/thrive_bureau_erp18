import { beforeEach, describe, expect, test } from "@thrive/hoot";
import { getService, makeMockEnv } from "@web/../tests/web_test_helpers";

describe.current.tags("headless");

let titleService;

beforeEach(async () => {
    await makeMockEnv();
    titleService = getService("title");
});

test("simple title", () => {
    titleService.setParts({ one: "MyThrive" });
    expect(titleService.current).toBe("MyThrive");
});

test("add title part", () => {
    titleService.setParts({ one: "MyThrive", two: null });
    expect(titleService.current).toBe("MyThrive");
    titleService.setParts({ three: "Import" });
    expect(titleService.current).toBe("MyThrive - Import");
});

test("modify title part", () => {
    titleService.setParts({ one: "MyThrive" });
    expect(titleService.current).toBe("MyThrive");
    titleService.setParts({ one: "Zopenerp" });
    expect(titleService.current).toBe("Zopenerp");
});

test("delete title part", () => {
    titleService.setParts({ one: "MyThrive" });
    expect(titleService.current).toBe("MyThrive");
    titleService.setParts({ one: null });
    expect(titleService.current).toBe("Thrive");
});

test("all at once", () => {
    titleService.setParts({ one: "MyThrive", two: "Import" });
    expect(titleService.current).toBe("MyThrive - Import");
    titleService.setParts({ one: "Zopenerp", two: null, three: "Sauron" });
    expect(titleService.current).toBe("Zopenerp - Sauron");
});

test("get title parts", () => {
    expect(titleService.current).toBe("");
    titleService.setParts({ one: "MyThrive", two: "Import" });
    expect(titleService.current).toBe("MyThrive - Import");
    const parts = titleService.getParts();
    expect(parts).toEqual({ one: "MyThrive", two: "Import" });
    parts.action = "Export";
    expect(titleService.current).toBe("MyThrive - Import"); // parts is a copy!
});
