"use client";

import { useTranslations } from "next-intl";
import { deleteFilePermanently } from "@/lib/files";

export function FileRow({ file }: { file: StoredFile }) {
  const t = useTranslations();

  return (
    <li className="row">
      <span>{file.name}</span>
      <button
        className="btn-danger"
        onClick={() => {
          if (confirm(t("common.confirmDelete", { name: file.name }))) {
            deleteFilePermanently(file.id);
          }
        }}
      >
        {t("common.remove")}
      </button>
    </li>
  );
}
