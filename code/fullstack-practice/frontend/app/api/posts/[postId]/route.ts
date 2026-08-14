import { revalidateTag } from "next/cache";
import { NextResponse } from "next/server";

export async function DELETE(
  _request: Request,
  { params }: { params: Promise<{ postId: string }> }
) {
  const fastapiUrl = process.env.FASTAPI_URL;

  if (!fastapiUrl) {
    return NextResponse.json(
      { detail: "FASTAPI_URL 환경 변수가 설정되지 않았습니다" },
      { status: 500 }
    );
  }

  const { postId } = await params;
  const res = await fetch(`${fastapiUrl}/posts/${postId}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    return NextResponse.json(
      { detail: error.detail ?? "게시글 삭제에 실패했습니다" },
      { status: res.status }
    );
  }

  revalidateTag("posts-list");
  return new NextResponse(null, { status: 204 });
}
